from typing import Union

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from demotodoapp.main.models import Note, Todo
from demotodoapp.main.services.todos.create import CreateTodoService
from demotodoapp.main.signals.signals import todo_created
from demotodoapp.permissions.decorators import check_permissions, Events
from demotodoapp.utils.handler import BaseHandler
from demotodoapp.utils.service_object import Error, Ok
from demotodoapp.utils.signal_mixin import SignalMixin

User = get_user_model()


class CreateTodoHandler(BaseHandler, SignalMixin):
    signal = todo_created
    signal_sender = Todo

    @check_permissions(event_code=Events.CREATE_TODO)
    def __init__(self, user: User, note: Note, text: str):
        self.user: User = user
        self.note: Note = note
        self.text: str = self._clean_text(text=text)

    def _clean_text(self, text: str) -> str:
        if len(text) > 120:
            raise self.exception(_("Todo text too long"))

        return text

    def run(self) -> Note:
        service: CreateTodoService = CreateTodoService()
        result: Union[Ok, Error] = service(
            note=self.note,
            text=self.text,
        )

        if result.is_error():
            raise self.exception(result.error)

        self._send_signal(todo=result.value.todo)

        return result.value.todo
