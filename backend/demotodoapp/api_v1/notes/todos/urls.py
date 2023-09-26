from django.urls import path

from demotodoapp.api_v1.notes.todos.views import TodosView, TodoView

app_name = "todos"

urlpatterns = [
    path("", TodosView.as_view()),
    path("<int:todo_id>/", TodoView.as_view()),
]
