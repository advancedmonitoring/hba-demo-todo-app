from typing import Union

from django.contrib.auth import get_user_model

from demotodoapp.main.models import Note
from demotodoapp.main.services.notes.delete import DeleteNoteService
from demotodoapp.main.signals.signals import note_deleted
from demotodoapp.permissions.decorators import Events, check_permissions
from demotodoapp.utils.handler import BaseHandler
from demotodoapp.utils.service_object import Ok, Error
from demotodoapp.utils.signal_mixin import SignalMixin

User = get_user_model()


class DeleteNoteHandler(BaseHandler, SignalMixin):
    signal = note_deleted
    signal_sender = Note

    @check_permissions(event_code=Events.DELETE_NOTE)
    def __init__(self, user: User, note: Note):
        self.user: User = user
        self.note: Note = note

    def run(self):
        note_id: int = self.note.id

        service: DeleteNoteService = DeleteNoteService()
        result: Union[Ok, Error] = service(note=self.note)

        if result.is_error():
            raise self.exception(result.error)

        self._send_signal(note_id=note_id, author_id=self.user.id)
        return None
