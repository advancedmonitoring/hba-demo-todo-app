from typing import Union

from django.contrib.auth import get_user_model

from demotodoapp.main.handlers.todos.data_handler import TodoDataHandler
from demotodoapp.main.models import Note, Todo
from demotodoapp.main.services.todos.delete import DeleteTodoService
from demotodoapp.main.signals.signals import todo_deleted
from demotodoapp.permissions.decorators import Events, check_permissions
from demotodoapp.utils.handler import BaseHandler
from demotodoapp.utils.service_object import Error, Ok
from demotodoapp.utils.signal_mixin import SignalMixin

User = get_user_model()


class DeleteTodoHandler(BaseHandler, SignalMixin):
    data_handler = TodoDataHandler
    signal = todo_deleted
    signal_sender = Todo

    @check_permissions(event_code=Events.DELETE_TODO)
    def __init__(self, user: User, note: Note, todo: Todo):
        self.user: User = user
        self.note: Note = note
        self.todo: Todo = todo

    def run(self):
        todo_id: int = self.todo.id
        note_id: int = self.todo.note_id  # noqa

        service: DeleteTodoService = DeleteTodoService()
        result: Union[Ok, Error] = service(todo=self.todo)

        if result.is_error():
            raise self.exception(result.error)

        self._send_signal(todo_id=todo_id, note_id=note_id)
        return None
