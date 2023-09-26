from django.utils.translation import gettext_lazy as _

from demotodoapp.main.models import Todo
from demotodoapp.utils.handler import BaseDataHandler


class TodoDataHandler(BaseDataHandler):
    def _prepare_todo_id(self):
        try:
            return Todo.objects.get(note=self.note, pk=self.todo_id)
        except Todo.DoesNotExist:
            raise self.handler.exception(_("Todo not found"))
