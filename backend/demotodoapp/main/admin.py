from django.contrib import admin

from demotodoapp.main.models import Note, Todo
from demotodoapp.utils.utils import linkify


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", linkify("author"), "name")
    list_filter = ("author", )


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("id", linkify("note"), "text")
    list_filter = ("note", "note__author")
