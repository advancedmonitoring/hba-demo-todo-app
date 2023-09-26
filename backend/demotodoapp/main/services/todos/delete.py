from typing import Union

from demotodoapp.main.models import Todo
from demotodoapp.utils.service_object import ServiceObject, transactional, service_call, Ok, Error


class DeleteTodoService(ServiceObject):
    def delete(self, context):
        context.todo.delete()
        return self.success()

    @transactional
    @service_call
    def __call__(self, todo: Todo) -> Union[Ok, Error]:
        return self.success(todo=todo) | self.delete
