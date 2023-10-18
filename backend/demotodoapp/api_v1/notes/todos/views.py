from django.utils.translation import gettext_lazy as _
from drf_rw_serializers.generics import ListAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination

from demotodoapp.api_v1.handlers_views import HandlerView
from demotodoapp.api_v1.notes.todos.serializers import (
    ReadTodoSerializer,
    WriteGetTodoSerializer,
    WriteUpdateTodoSerializer,
    WriteAddTodoSerializer,
)
from demotodoapp.api_v1.serializers import DummyDetailSerializer, DummyDetailAndStatusSerializer
from demotodoapp.main.handlers.todos.create import CreateTodoHandler
from demotodoapp.main.handlers.todos.delete import DeleteTodoHandler
from demotodoapp.main.handlers.todos.get import GetTodosHandler, GetTodoHandler
from demotodoapp.main.handlers.todos.update import UpdateTodoHandler


@extend_schema(tags=["Todos"])
@extend_schema_view(
    post=extend_schema(
        request=WriteAddTodoSerializer,
        responses={
            status.HTTP_201_CREATED: ReadTodoSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    ),
    get=extend_schema(
        responses={
            status.HTTP_200_OK: ReadTodoSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
)
class TodosView(HandlerView, ListAPIView):
    pagination_class = PageNumberPagination
    pagination_class.page_size_query_param = "limit"
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id", "text", "done"]

    def post(self, request, *args, **kwargs):
        """ Создание задачи """
        self.serializer_class = WriteAddTodoSerializer
        self.error_text = _("Create todo error")
        self.read_serializer_class = ReadTodoSerializer
        self.response_code = status.HTTP_201_CREATED
        self.handler = CreateTodoHandler
        return self.handle()

    def get_queryset(self):
        """ Получение списка задач из записи """
        self.response_code = status.HTTP_200_OK
        self.handler = GetTodosHandler
        self.read_serializer_class = ReadTodoSerializer
        self.error_text = _("Get todos error")
        return self.get_handler_result()


@extend_schema(tags=["Todos"])
class TodoView(HandlerView):
    @extend_schema(
        request=WriteGetTodoSerializer,
        responses={
            status.HTTP_200_OK: ReadTodoSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """ Получение информации о записи """
        self.response_code = status.HTTP_200_OK
        self.serializer_class = WriteGetTodoSerializer
        self.error_text = _("Get note error")
        self.read_serializer_class = ReadTodoSerializer
        self.handler = GetTodoHandler
        return self.handle()

    @extend_schema(
        request=WriteUpdateTodoSerializer,
        responses={
            status.HTTP_200_OK: ReadTodoSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
    def patch(self, request, *args, **kwargs):
        """ Изменение задачи """
        self.response_code = status.HTTP_200_OK
        self.serializer_class = WriteUpdateTodoSerializer
        self.read_serializer_class = ReadTodoSerializer
        self.error_text = _("Update todo error")
        self.handler = UpdateTodoHandler
        return self.handle()

    @extend_schema(
        request=WriteGetTodoSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
    def delete(self, request, *args, **kwargs):
        """ Удаление задачи """
        self.response_code = status.HTTP_204_NO_CONTENT
        self.serializer_class = WriteGetTodoSerializer
        self.error_text = _("Delete todo error")
        self.handler = DeleteTodoHandler
        return self.handle()
