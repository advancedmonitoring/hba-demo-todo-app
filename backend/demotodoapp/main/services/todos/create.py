from typing import Union

from django.contrib.auth import get_user_model

from demotodoapp.main.models import Note, Todo
from demotodoapp.utils.service_object import ServiceObject, transactional, service_call, Error, Ok

User = get_user_model()


class CreateTodoService(ServiceObject):
    def create_todo(self, context):
        todo: Todo = Todo.objects.create(
            note=context.note,
            text=context.text,
            done=False,
        )

        return self.success(todo=todo)

    @transactional
    @service_call
    def __call__(self, note: Note, text: str) -> Union[Ok, Error]:
        return self.success(note=note, text=text) | \
               self.create_todo
