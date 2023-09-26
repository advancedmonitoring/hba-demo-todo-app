from typing import Union

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from demotodoapp.main.models import Note
from demotodoapp.main.services.notes.create import CreateNoteService
from demotodoapp.main.signals.signals import note_created
from demotodoapp.permissions.decorators import Events, check_permissions
from demotodoapp.utils.handler import BaseHandler
from demotodoapp.utils.service_object import Ok, Error
from demotodoapp.utils.signal_mixin import SignalMixin

User = get_user_model()


class CreateNoteHandler(BaseHandler, SignalMixin):
    signal = note_created
    signal_sender = Note

    @check_permissions(event_code=Events.CREATE_NOTE)
    def __init__(self, user: User, name: str):
        self.user: User = user
        self.name: str = self._clean_name(name=name)

    def _clean_name(self, name: str) -> str:
        if len(name) > 30:
            raise self.exception(_("Note name too long"))

        return name

    def run(self) -> Note:
        service: CreateNoteService = CreateNoteService()
        result: Union[Ok, Error] = service(
            author=self.user,
            name=self.name,
        )

        if result.is_error():
            raise self.exception(result.error)

        self._send_signal(note=result.value.note)

        return result.value.note
