from django.contrib.auth import get_user_model

from demotodoapp.main.handlers.todos.data_handler import TodoDataHandler
from demotodoapp.main.models import Todo, Note
from demotodoapp.permissions.decorators import check_permissions, Events
from demotodoapp.utils.handler import BaseHandler
from demotodoapp.utils.utils import QueryType

User = get_user_model()


class GetTodosHandler(BaseHandler):

    @check_permissions(event_code=Events.GET_TODOS)
    def __init__(self, user: User, note: Note):
        self.user: User = user
        self.note: Note = note

    def run(self) -> QueryType[Todo]:
        return self.note.todos.all()


class GetTodoHandler(BaseHandler):
    data_handler = TodoDataHandler

    @check_permissions(event_code=Events.GET_TODO)
    def __init__(self, user: User, note: Note, todo: Todo):
        self.user: User = user
        self.note: Note = note
        self.todo: Todo = todo

    def run(self) -> Todo:
        return self.todo
