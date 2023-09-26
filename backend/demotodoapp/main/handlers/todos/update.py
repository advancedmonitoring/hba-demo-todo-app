from typing import Union

from django.contrib.auth import get_user_model

from demotodoapp.main.handlers.todos.data_handler import TodoDataHandler
from demotodoapp.main.models import Note, Todo
from demotodoapp.main.services.todos.update import UpdateTodoService
from demotodoapp.main.signals.signals import todo_updated
from demotodoapp.permissions.decorators import Events, check_permissions
from demotodoapp.utils.handler import BaseHandler
from demotodoapp.utils.handler_validation_mixin import ValidationMixin
from demotodoapp.utils.service_object import Error, Ok
from demotodoapp.utils.signal_mixin import SignalMixin

User = get_user_model()


class UpdateTodoHandler(BaseHandler, SignalMixin, ValidationMixin):
    data_handler = TodoDataHandler
    signal = todo_updated
    signal_sender = Todo

    @check_permissions(event_code=Events.UPDATE_TODO)
    def __init__(self, user: User, note: Note, todo: Todo, **kwargs):
        self.user: User = user
        self.note: Note = note
        self.todo: Todo = todo
        self.validate(**kwargs)

    def run(self) -> Todo:
        service: UpdateTodoService = UpdateTodoService()
        result: Union[Ok, Error] = service(
            todo=self.todo,
            **self.validated_data,
        )

        if result.is_error():
            raise self.exception(result.error)
        self._send_signal(todo=self.todo)

        return self.todo
