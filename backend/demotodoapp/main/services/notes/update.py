from typing import Union

from demotodoapp.main.models import Note
from demotodoapp.utils.service_object import ServiceObject, service_call, transactional, Ok, Error


class UpdateNoteService(ServiceObject):

    def update(self, context):
        note: Note = context.note
        for attr, value in context.params.items():
            setattr(note, attr, value)

        note.save()

        return self.success()

    @transactional
    @service_call
    def __call__(self, note: Note, **kwargs) -> Union[Ok, Error]:
        return self.success(note=note, params=kwargs) | self.update
