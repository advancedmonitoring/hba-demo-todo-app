from django.dispatch import receiver

from demotodoapp.api_v1.notes.serializers import ReadNoteSerializer
from demotodoapp.api_v1.notes.todos.serializers import ReadTodoSerializer
from demotodoapp.main.models import Note, Todo
from demotodoapp.main.signals.signals import (
    note_created,
    note_updated,
    note_deleted,
    todo_created,
    todo_updated,
    todo_deleted,
)
from demotodoapp.ws_v1.utils import get_user_ws_group_name, send_to_socket_group, get_note_ws_group_name


def send_note(note: Note, event: str):
    group_name: str = get_user_ws_group_name(user_id=note.author_id)  # noqa

    send_to_socket_group(
        group_name=group_name,
        event=event,
        **ReadNoteSerializer(note).data,
    )


@receiver(note_created, sender=Note)
def share_note_created(sender, note: Note, **kwargs):
    send_note(note=note, event="note_created")


@receiver(note_updated, sender=Note)
def share_note_updated(sender, note: Note, **kwargs):
    send_note(note=note, event="note_updated")


@receiver(note_deleted, sender=Note)
def share_note_deleted(sender, note_id: int, author_id: int, **kwargs):
    group_name: str = get_user_ws_group_name(user_id=author_id)
    send_to_socket_group(
        group_name=group_name,
        event="note_deleted",
        note_id=note_id,
    )


def send_todo(todo: Todo, event: str):
    group_name: str = get_note_ws_group_name(note_id=todo.note_id)  # noqa

    send_to_socket_group(
        group_name=group_name,
        event=event,
        **ReadTodoSerializer(todo).data,
    )


@receiver(todo_created, sender=Todo)
def share_todo_created(sender, todo: Todo, **kwargs):
    send_todo(todo=todo, event="todo_created")


@receiver(todo_updated, sender=Todo)
def share_todo_updated(sender, todo: Todo, **kwargs):
    send_todo(todo=todo, event="todo_updated")


@receiver(todo_deleted, sender=Todo)
def share_todo_deleted(sender, todo_id: int, note_id: int, **kwargs):
    group_name: str = get_note_ws_group_name(note_id=note_id)
    send_to_socket_group(
        group_name=group_name,
        event="todo_deleted",
        todo_id=todo_id,
    )

