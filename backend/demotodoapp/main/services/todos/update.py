from typing import Union

from demotodoapp.main.models import Todo
from demotodoapp.utils.service_object import ServiceObject, service_call, transactional, Error, Ok


class UpdateTodoService(ServiceObject):

    def update(self, context):
        todo: Todo = context.todo
        for attr, value in context.params.items():
            setattr(todo, attr, value)

        todo.save()

        return self.success()

    @transactional
    @service_call
    def __call__(self, todo: Todo, **kwargs) -> Union[Ok, Error]:
        return self.success(todo=todo, params=kwargs) | self.update
