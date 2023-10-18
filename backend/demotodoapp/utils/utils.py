import logging
from pathlib import Path
from typing import Generic, Iterator, TypeVar

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.html import format_html

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
