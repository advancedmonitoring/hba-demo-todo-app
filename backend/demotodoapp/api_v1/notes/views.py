from django.utils.translation import gettext_lazy as _
from drf_rw_serializers.generics import ListAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, status

from demotodoapp.api_v1.handlers_views import HandlerView
from demotodoapp.api_v1.notes.serializers import (
    ReadNoteSerializer,
    WriteAddNoteSerializer,
    WriteGetNoteSerializer,
    WriteUpdateNoteSerializer,
)
from demotodoapp.api_v1.serializers import DummyDetailSerializer, DummyDetailAndStatusSerializer
from demotodoapp.main.handlers.notes.create import CreateNoteHandler
from demotodoapp.main.handlers.notes.delete import DeleteNoteHandler
from demotodoapp.main.handlers.notes.get import GetNoteHandler, GetNotesHandler
from demotodoapp.main.handlers.notes.update import UpdateNoteHandler
from demotodoapp.main.models import Note


@extend_schema(tags=["Notes"])
@extend_schema_view(
    post=extend_schema(
        request=WriteAddNoteSerializer,
        responses={
            status.HTTP_201_CREATED: ReadNoteSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    ),
    get=extend_schema(
        responses={
            status.HTTP_200_OK: ReadNoteSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
)
class NotesView(HandlerView, ListAPIView):
    queryset = Note.objects.none()  # только для swagger схемы
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]
    ordering = ["id"]

    def post(self, request, *args, **kwargs):
        """ Создание записи """
        self.serializer_class = WriteAddNoteSerializer
        self.error_text = _("Create note error")
        self.read_serializer_class = ReadNoteSerializer
        self.response_code = status.HTTP_201_CREATED
        self.handler = CreateNoteHandler
        return self.handle()

    def get_queryset(self):
        """Получение множества объектов Notes."""
        self.error_text = _("Get notes error")
        self.read_serializer_class = ReadNoteSerializer
        self.response_code = status.HTTP_200_OK
        self.handler = GetNotesHandler
        return self.get_handler_result()


@extend_schema(tags=["Notes"])
class NoteView(HandlerView):
    @extend_schema(
        request=WriteGetNoteSerializer,
        responses={
            status.HTTP_200_OK: ReadNoteSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """ Получение информации о записи """
        self.response_code = status.HTTP_200_OK
        self.serializer_class = WriteGetNoteSerializer
        self.error_text = _("Get note error")
        self.read_serializer_class = ReadNoteSerializer
        self.handler = GetNoteHandler
        return self.handle()

    @extend_schema(
        request=WriteUpdateNoteSerializer,
        responses={
            status.HTTP_200_OK: ReadNoteSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
    def patch(self, request, *args, **kwargs):
        """ Изменение записи """
        self.response_code = status.HTTP_200_OK
        self.serializer_class = WriteUpdateNoteSerializer
        self.read_serializer_class = ReadNoteSerializer
        self.error_text = _("Update note error")
        self.handler = UpdateNoteHandler
        return self.handle()

    @extend_schema(
        request=WriteGetNoteSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
    def delete(self, request, *args, **kwargs):
        """ Удаление записи """
        self.response_code = status.HTTP_204_NO_CONTENT
        self.serializer_class = WriteGetNoteSerializer
        self.error_text = _("Delete note error")
        self.handler = DeleteNoteHandler
        return self.handle()
