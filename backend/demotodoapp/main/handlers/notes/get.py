from django.contrib.auth import get_user_model

from demotodoapp.main.models import Todo, Note
from demotodoapp.permissions.decorators import check_permissions, Events
from demotodoapp.utils.handler import BaseHandler
from demotodoapp.utils.utils import QueryType

User = get_user_model()


class GetNotesHandler(BaseHandler):

    @check_permissions(event_code=Events.GET_NOTES)
    def __init__(self, user: User):
        self.user: User = user

    def run(self) -> QueryType[Note]:
        return Note.objects.filter(author=self.user)


class GetNoteHandler(BaseHandler):

    @check_permissions(event_code=Events.GET_NOTE)
    def __init__(self, user: User, note: Note):
        self.user: User = user
        self.note: Note = note

    def run(self) -> Note:
        return self.note
