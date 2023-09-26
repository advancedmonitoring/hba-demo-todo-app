from typing import Union

from django.contrib.auth import get_user_model

from demotodoapp.main.models import Note
from demotodoapp.utils.service_object import ServiceObject, transactional, service_call, Error, Ok

User = get_user_model()


class CreateNoteService(ServiceObject):
    def create_note(self, context):
        note: Note = Note.objects.create(
            author=context.author,
            name=context.name,
        )

        return self.success(note=note)

    @transactional
    @service_call
    def __call__(self, author: User, name: str) -> Union[Ok, Error]:
        return self.success(author=author, name=name) | \
               self.create_note
