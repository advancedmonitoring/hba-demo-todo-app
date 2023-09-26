from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from demotodoapp.main.models import Note
from demotodoapp.utils.constants import NOTE_NAME_MAX_LENGTH


class WriteGetNoteSerializer(serializers.Serializer):
    pass


class WriteUpdateNoteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=NOTE_NAME_MAX_LENGTH,
                                 label=_("name"))


class WriteAddNoteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=NOTE_NAME_MAX_LENGTH,
                                 label=_("name"))


class ReadNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("id", "author_id", "name")
