from typing import Type

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from demotodoapp.api_v1.notes.serializers import ReadNoteSerializer
from demotodoapp.api_v1.notes.todos.serializers import ReadTodoSerializer
from demotodoapp.main.handlers.todos.get import GetTodosHandler
from demotodoapp.main.models import Note
from demotodoapp.utils.handler import BaseHandler

User = get_user_model()


def get_data(obj, serializer=None):
    def _wrapper():
        if serializer is not None:
            serialized_object = serializer(obj)
            return serialized_object.data

        return obj.data

    return sync_to_async(_wrapper)()


class OpenNoteHandler:
    def __init__(self, consumer):
        self.consumer = consumer
        self.user: User = consumer.user
        self.note: Note = consumer.note

    @database_sync_to_async
    def _prepare_data(self, handler: Type[BaseHandler], serializer, many: bool = True, **kwargs):
        result = handler(user=self.user, note=self.note, **kwargs).run()  # noqa

        serializer = serializer(result, context={"user": self.user}, many=many)
        return serializer.data

    async def send_data(self):
        await self.send_note_data()
        await self.send_todos()

        await self.send_load_end()

    async def send_note_data(self):
        data = await get_data(self.note, serializer=ReadNoteSerializer)
        await self.consumer.send_note_data(note_data=data)

    async def send_todos(self):
        data = await self._prepare_data(handler=GetTodosHandler, serializer=ReadTodoSerializer)
        await self.consumer.send_todos(todos=data)

    async def send_load_end(self):
        await self.consumer.send_note_load_end()
