from django.urls import path, include

from demotodoapp.api_v1.notes.views import NotesView, NoteView

app_name = "notes"

urlpatterns = [
    path("", NotesView.as_view()),
    path("<int:note_id>/", NoteView.as_view()),
    path("<int:note_id>/todos/", include("demotodoapp.api_v1.notes.todos.urls", namespace="todos")),
]
