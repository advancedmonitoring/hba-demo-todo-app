from typing import Union

from django.contrib.auth import get_user_model

from demotodoapp.main.models import Note
from demotodoapp.main.services.notes.update import UpdateNoteService
from demotodoapp.main.signals.signals import note_updated
from demotodoapp.permissions.decorators import Events, check_permissions
from demotodoapp.utils.handler import BaseHandler
from demotodoapp.utils.handler_validation_mixin import ValidationMixin
from demotodoapp.utils.service_object import Ok, Error
from demotodoapp.utils.signal_mixin import SignalMixin

User = get_user_model()


class UpdateNoteHandler(BaseHandler, SignalMixin, ValidationMixin):
    signal = note_updated
    signal_sender = Note

    @check_permissions(event_code=Events.UPDATE_NOTE)
    def __init__(self, user: User, note: Note, **kwargs):
        self.user: User = user
        self.note: Note = note
        self.validate(**kwargs)

    def run(self) -> Note:
        service: UpdateNoteService = UpdateNoteService()
        result: Union[Ok, Error] = service(
            note=self.note,
            **self.validated_data,
        )

        if result.is_error():
            raise self.exception(result.error)

        self._send_signal(note=self.note)

        return self.note
