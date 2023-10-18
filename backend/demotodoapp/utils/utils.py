import logging
from pathlib import Path
from typing import Generic, Iterator, TypeVar, List

from django.conf import settings
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.http import Http404
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.html import format_html
from rest_framework import status
from rest_framework.exceptions import APIException, NotAuthenticated
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def validate_file_extension(*extensions):
    def wrapper(value):
        """
        Проверяет соответствие расширения файла допустимым расширениям.
        Валидатор используется для полей модели.
        Если расширение файла не соответствует допустимому, то возникает ошибка ValidationError.
        """
        file = Path(value.path)
        file_extension = file.suffix
        if file_extension not in extensions:
            raise ValidationError("File not supported!")

    return wrapper


T = TypeVar("T")


class QueryType(Generic[T], QuerySet):
    def __iter__(self) -> Iterator[T]: ...


def first(ordered_dict):
    """
    Возвращает первый элемент из упорядоченной коллекции
    или произвольный элемент из неупорядоченной коллекции.
    Если коллекция пуста, вызывается исключение StopIteration.
    """
    return next(iter(ordered_dict))


def get_field_label(field_name, serializer):
    fields = serializer().fields
    if field_name in fields:
        return fields[field_name].label


def exception_handler(exc, context=None):
    """Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's builtin `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """

    if isinstance(exc, APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header  # noqa
        if getattr(exc, "wait", None):
            headers["X-Throttle-Wait-Seconds"] = "%d" % exc.wait  # noqa

        detail = format_exception(exc)

        response = Response(detail, status=exc.status_code, headers=headers)

        if isinstance(exc, NotAuthenticated):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            # response.data["status_code"] = status.HTTP_401_UNAUTHORIZED

        return response

    elif isinstance(exc, Http404):
        return Response(
            {"error_type": exc.__class__.__name__, "errors": [{"message": str(exc)}]},
            status=status.HTTP_404_NOT_FOUND,
        )

    elif isinstance(exc, DjangoPermissionDenied):
        return Response(
            {"error_type": exc.__class__.__name__, "errors": [{"message": str(exc)}]},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Note: Unhandled exceptions will raise a 500 error.
    return None


def format_exception(exc):
    class_name = exc.__class__.__name__
    detail = {"errors": [], "error_type": class_name}
    if isinstance(exc.detail, dict):
        for error_key, error_values in list(exc.detail.items()):
            if isinstance(error_values, dict):
                # For the cases of nested field e.g. ListField and the error is in
                # validating one of the child items.
                detail["errors"].append(
                    {
                        "field": error_key,
                        "message": "Validation failed for one of the item in the list.",
                        "errors": [
                            {
                                "field": error_key,
                                "message": ", ".join(error_msg)
                                if isinstance(error_msg, list)
                                else error_msg,
                            }
                            for error_key, error_msg in error_values.items()
                        ],
                    },
                )
            else:
                if any(isinstance(item, List) for item in error_values):
                    detail["errors"] = detail["errors"] + parse_field_errors(
                        error_key, None, error_values,
                    )
                else:
                    for error_msg in error_values:
                        # Special Case for model clean
                        if error_key == "non_field_errors":
                            detail["errors"].append({"message": error_msg})
                        else:
                            detail["errors"] = detail["errors"] + parse_field_errors(
                                error_key, error_msg, error_values,
                            )
    elif isinstance(exc.detail, list):
        for error_msg in exc.detail:
            detail["errors"].append({"message": error_msg})
    else:
        detail["errors"].append({"message": force_str(exc.detail)})

    return detail


def parse_field_errors(field, error_msg, error_values, depth=0):
    # We only parse errors upto 10 nested serializers
    if depth is not None:
        assert depth >= 0, "'depth' may not be negative."
        assert depth <= 10, "'depth' may not be greater than 10."

    errors = []

    if error_msg is None or isinstance(error_msg, dict):
        field_errors = {
            "field": field,
            "message": None,
            "errors": [],
        }

        if error_msg is None:
            for error in error_values:
                field_errors["errors"].append(error or [])
        else:
            for error_msg_key, error_msg_values in list(error_msg.items()):
                for msg in error_msg_values:
                    field_errors["errors"].extend(parse_field_errors(
                        error_msg_key, msg, error_values, depth=depth + 1,
                    ))

        errors.append(field_errors)
        return errors

    errors.append(
        {
            "field": error_msg
            if error_msg and error_values and type(error_values) != list
            else field,
            "message": " ".join(error_values[error_msg])
            if error_msg and error_values and type(error_values) != list
            else error_msg,
        },
    )
    return errors


def linkify(field_name):
    """
    Преобразует значение внешнего ключа в кликабельные ссылки.

    Если field_name == 'parent', то текст ссылки будет (obj.parent)
    Ссылка будет иметь вид admin_url для obj.parent.id:change
    """

    def _linkify(obj):
        try:
            linked_obj = getattr(obj, field_name)
            if linked_obj is None:
                return "-"
            app_label = linked_obj._meta.app_label
            model_name = linked_obj._meta.model_name
            view_name = f"admin:{app_label}_{model_name}_change"
            link_url = reverse(view_name, args=[linked_obj.pk])
            return format_html('<a href="{}">{}</a>', link_url, linked_obj)
        except Exception:  # noqa BLE001
            return getattr(obj, field_name)

    _linkify.short_description = field_name  # Sets column name
    return _linkify


def get_file_format_choices():
    format_choices = []
    for file_suffix in settings.SUPPORTED_FORMATS:
        file_format = file_suffix[1:]
        format_choices.append((file_format, file_format))
    return format_choices
