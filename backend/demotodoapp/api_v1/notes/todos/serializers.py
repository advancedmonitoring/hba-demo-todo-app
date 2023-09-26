from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from demotodoapp.main.models import Todo
from demotodoapp.utils.constants import TODO_TEXT_MAX_LENGTH


class WriteGetTodoSerializer(serializers.Serializer):
    pass


class WriteUpdateTodoSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=TODO_TEXT_MAX_LENGTH,
                                 required=False,
                                 label=_("text"))
    done = serializers.BooleanField(required=False, label=_("done"))


class WriteAddTodoSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=TODO_TEXT_MAX_LENGTH,
                                 label=_("text"))


class ReadTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ("id", "note_id", "text", "done")
