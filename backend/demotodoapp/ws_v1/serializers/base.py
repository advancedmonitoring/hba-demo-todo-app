from rest_framework import serializers

from demotodoapp.api_v1.notes.serializers import ReadNoteSerializer
from demotodoapp.api_v1.notes.todos.serializers import ReadTodoSerializer


class NotificationSerializer(serializers.Serializer):
    message = serializers.CharField()
    type = serializers.CharField()
    title = serializers.CharField()
    extra = serializers.DictField()


class OpenNoteEventSerializer(serializers.Serializer):
    note_id = serializers.IntegerField()


class CloseNoteEventSerializer(serializers.Serializer):
    pass


class TodoSerializer(ReadTodoSerializer):
    pass


class NoteSerializer(ReadNoteSerializer):
    pass


class NoteDeletedSerializer(serializers.Serializer):
    note_id = serializers.IntegerField()


class NoteLoadEndSerializer(serializers.Serializer):
    pass


class TodoDeletedSerializer(serializers.Serializer):
    todo_id = serializers.IntegerField()


class UserOnlineStatusChangedSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    is_online = serializers.BooleanField()
