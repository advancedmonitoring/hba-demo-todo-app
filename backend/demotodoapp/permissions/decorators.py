import enum
from functools import wraps

from django.contrib.auth import get_user_model

from demotodoapp.permissions.permissions import EventPermissions

User = get_user_model()


class Events(enum.Enum):
    GET_NOTE = "get_note"
    GET_NOTES = "get_notes"
    CREATE_NOTE = "create_note"
    UPDATE_NOTE = "update_note"
    DELETE_NOTE = "delete_note"

    GET_TODO = "get_todo"
    GET_TODOS = "get_todos"
    CREATE_TODO = "create_todo"
    UPDATE_TODO = "update_todo"
    DELETE_TODO = "delete_todo"


class PermissionsDenied(Exception):
    pass


def check_permissions(event_code: Events):
    def wrapper(func):

        @wraps(func)
        def check_permission(handler, *args, **kwargs):
            if args:
                raise ValueError("Pass only keyword args for permissions check")

            user = kwargs.get("user")

            if user is None:
                raise ValueError("Pass user to check permissions")

            func(handler, **kwargs)
            checker = EventPermissions(user, event_code, kwargs)
            granted: bool = checker()

            if granted is False:
                raise PermissionsDenied(checker.get_denied_message())

        return check_permission

    return wrapper
