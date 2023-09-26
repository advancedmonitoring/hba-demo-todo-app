from typing import Union

from demotodoapp.main.models import Note
from demotodoapp.utils.service_object import ServiceObject, transactional, service_call, Error, Ok


class DeleteNoteService(ServiceObject):
    def delete(self, context):
        context.note.delete()
        return self.success()

    @transactional
    @service_call
    def __call__(self, note: Note) -> Union[Ok, Error]:
        return self.success(note=note) | self.delete
