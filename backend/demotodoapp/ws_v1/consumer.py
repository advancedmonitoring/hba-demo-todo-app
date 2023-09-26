import logging
from typing import Any, Dict, Optional

from asgiref.sync import sync_to_async
from channels.consumer import get_handler_name
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from demotodoapp.api_v1.serializers import EmptySerializer
from demotodoapp.main.handlers.notes.get import GetNoteHandler
from demotodoapp.main.models import Note
from demotodoapp.permissions.decorators import PermissionsDenied
from demotodoapp.utils.attrdict import AttrDict
from demotodoapp.ws_v1.handlers.connected import UserConnectedHandler
from demotodoapp.ws_v1.handlers.open_note import OpenNoteHandler
from demotodoapp.ws_v1.schema.decorators import extend_ws_schema
from demotodoapp.ws_v1.serializers.base import (
    NotificationSerializer,
    OpenNoteEventSerializer,
    CloseNoteEventSerializer,
    TodoSerializer,
    NoteSerializer,
    NoteLoadEndSerializer,
    NoteDeletedSerializer,
    TodoDeletedSerializer,
    UserOnlineStatusChangedSerializer
)
from demotodoapp.ws_v1.utils import (
    get_user_ws_group_name,
    get_global_ws_group_name,
    get_note_ws_group_name,
    Connections,
)

User = get_user_model()
logger = logging.getLogger(__name__)


class Consumer(AsyncJsonWebsocketConsumer):
    __user: Optional[User] = None
    __note: Optional[Note] = None

    async def receive_json(self, content, **kwargs):
        """
        Диспетчер, обрабатывающий входящий json. В нем есть event по которому определяется
        какой метод надо запустить для обработки этого сообщения
        :param content: Словарь { event, data }
        :param kwargs: Остальные параметры
        :return: None

        """
        content = AttrDict(content)

        if not hasattr(self, content.event):
            logger.warning(f"NO HANDLER FOR {content.event} event!!!")
            return

        await self.process_message(event=content.event, data=content.get("data", {}))

    async def process_message(self, event, data):
        try:
            handler = getattr(self, event)
            res = await handler(**data)

        except Exception as e:
            logger.exception(e)
            await self.send_notify(message=_("Request error"), status="error")

        else:
            if res:
                await self.send_notify(message=res, status="warning")

    async def dispatch(self, message):
        """
        Dispatches incoming messages to type-based handler.
        """

        handler_name: str = get_handler_name(message)
        handler = getattr(self, handler_name, None)

        if handler:
            if handler_name.startswith("websocket"):
                await handler(message)
            else:
                await handler(**message.get("data", {}))
        else:
            raise ValueError("No handler for message type %s" % message["type"])

    @extend_ws_schema(
        type="receive",
        event="notify",
        description="Retrieve notification",
        request=EmptySerializer,
        responses=NotificationSerializer,
    )
    async def send_notify(self, message: str, status: str, title: Optional[str] = None, extra: Optional[Dict] = None):
        if extra is None:
            extra = {}

        await self.send_data(event="notify", message=message, type=status, title=title, extra=extra)

    @property
    def user(self) -> Optional[User]:
        return self.__user

    @user.setter
    def user(self, _) -> None:
        return

    def set_user(self, user: User) -> None:
        self.__user = user

    @property
    def note(self) -> Optional[Note]:
        return self.__note

    @note.setter
    def note(self, _) -> None:
        return

    def set_note(self, note: Optional[Note]) -> None:
        self.__note = note

    async def send_data(self, event: str, **kwargs: Any) -> None:
        await self.send_json({
            "event": event,
            "data": kwargs,
        })

    async def add_user_groups(self) -> None:
        if self.__user is not None and not self.__user.is_anonymous:
            await self.__add_group(name=get_user_ws_group_name(user_id=self.__user.id))

        await self.__add_group(name=get_global_ws_group_name())

    async def discard_user_groups(self) -> None:
        if self.__user is not None and not self.__user.is_anonymous:
            await self.__discard_group(name=get_user_ws_group_name(user_id=self.__user.id))

        await self.__discard_group(name=get_global_ws_group_name())

    async def __add_group(self, name: str) -> None:
        await self.channel_layer.group_add(name, self.channel_name)

    async def __discard_group(self, name: str) -> None:
        await self.channel_layer.group_discard(name, self.channel_name)

    async def connect(self):
        user = self.scope["user"]

        if user.is_anonymous:
            return self.close()

        self.set_user(user=user)
        await self.add_user_groups()
        await self.accept()

        await sync_to_async(Connections.user_connected)(user=user, channel_name=self.channel_name)
        await UserConnectedHandler(consumer=self).send_data()

    async def disconnect(self, code):
        user = self.scope["user"]
        await sync_to_async(Connections.user_disconnected)(user=user, channel_name=self.channel_name)
        await self.discard_user_groups()

    @database_sync_to_async
    def _get_note(self, note_id: int):
        data = GetNoteHandler.prepare_data(user=self.user, data={"note_id": note_id})
        handler = GetNoteHandler(**data)
        return handler.run()

    @extend_ws_schema(
        type="send",
        description="Open note event handler",
        request=OpenNoteEventSerializer,
        responses=["note_data", "todos", "note_load_end"],
    )
    async def open_note(self, note_id: int):
        try:
            note = await self._get_note(note_id=note_id)

        except GetNoteHandler.exception as exc:
            await self.send_notify(message=str(exc), status="error")
            await self.close_note()

        except PermissionsDenied:
            await self.send_notify(message=_("You have no permissions to open note"), status="error")
            await self.close_note()

        else:
            self.set_note(note=note)
            await self.__add_group(name=get_note_ws_group_name(note_id=note_id))

            await OpenNoteHandler(self).send_data()

    @extend_ws_schema(
        type="send",
        description="Close note event handler",
        request=CloseNoteEventSerializer,
        responses=CloseNoteEventSerializer,
    )
    async def close_note(self):
        await self.send_data(event="close_note")
        if not self.note:
            return

        note_id = self.note.id

        self.set_note(note=None)
        await self.__discard_group(name=get_note_ws_group_name(note_id=note_id))

    @extend_ws_schema(
        type="receive",
        event="todos",
        description="Retrieve todos on open note",
        request=EmptySerializer,
        responses=TodoSerializer(many=True),
    )
    async def send_todos(self, todos):
        await self.send_data(
            event="todos",
            todos=todos,
        )

    @extend_ws_schema(
        type="receive",
        event="note_data",
        description="Retrieve note data on open",
        request=EmptySerializer,
        responses=NoteSerializer,
    )
    async def send_note_data(self, note_data):
        await self.send_data(
            event="note_data",
            **note_data,
        )

    @extend_ws_schema(
        type="receive",
        event="note_load_end",
        description="Retrieve after all note data received",
        request=EmptySerializer,
        responses=NoteLoadEndSerializer,
    )
    async def send_note_load_end(self):
        await self.send_data(event="note_load_end")

    @extend_ws_schema(
        type="receive",
        event="note_added",
        description="Event on new note create",
        request=EmptySerializer,
        responses=NoteSerializer,
    )
    async def note_created(self, **data):
        await self.send_data(
            event="note_added",
            **data,
        )

    @extend_ws_schema(
        type="receive",
        event="note_updated",
        description="Event on note update",
        request=EmptySerializer,
        responses=NoteSerializer,
    )
    async def note_updated(self, **data):
        await self.send_data(
            event="note_updated",
            **data,
        )

    @extend_ws_schema(
        type="receive",
        event="note_deleted",
        description="Event on note deleted",
        request=EmptySerializer,
        responses=NoteDeletedSerializer,
    )
    async def note_deleted(self, note_id: int):
        await self.send_data(
            event="note_deleted",
            note_id=note_id,
        )

    @extend_ws_schema(
        type="receive",
        event="todo_added",
        description="Event on new todo create",
        request=EmptySerializer,
        responses=TodoSerializer,
    )
    async def todo_created(self, **data):
        await self.send_data(
            event="todo_added",
            **data,
        )

    @extend_ws_schema(
        type="receive",
        event="todo_updated",
        description="Event on todo update",
        request=EmptySerializer,
        responses=TodoSerializer,
    )
    async def todo_updated(self, **data):
        await self.send_data(
            event="todo_updated",
            **data,
        )

    @extend_ws_schema(
        type="receive",
        event="todo_deleted",
        description="Event on todo delete",
        request=EmptySerializer,
        responses=TodoDeletedSerializer,
    )
    async def todo_deleted(self, todo_id: int):
        await self.send_data(
            event="todo_deleted",
            todo_id=todo_id,
        )

    @extend_ws_schema(
        type="receive",
        event="user_online_status_changed",
        description="Event on user online status change",
        request=EmptySerializer,
        responses=UserOnlineStatusChangedSerializer,
    )
    async def user_online_status_changed(self, user_id: int, is_online: bool):
        if self.user and self.user.id == user_id:
            return

        await self.send_data(
            event="user_online_status_changed",
            user_id=user_id,
            is_online=is_online,
        )
