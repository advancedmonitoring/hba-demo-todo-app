from typing import Any, Dict, List

from django.db.models import Model, QuerySet


class EagerLoadingMixin:
    select_related: List[Any] = []
    prefetch_related: List[Any] = []
    annotate: Dict[str, Any] = {}
    aggregate: Dict[str, Any] = {}

    def __init__(self, instance=None, *args, **kwargs):
        if isinstance(instance, Model):
            object_id = instance.id
            qs = self.setup_eager_loading(instance.__class__.objects.filter(id=object_id))
            instance = qs.first()

        super().__init__(*args, instance=instance, **kwargs)

    @classmethod
    def many_init(cls, instance=None, *args, **kwargs):
        if isinstance(instance, QuerySet):
            instance = cls.setup_eager_loading(instance)

        elif isinstance(instance, List):
            ids = [item.id for item in instance]

            if ids:
                qs = type(instance[0]).objects.filter(id__in=ids)
                qs = cls.setup_eager_loading(qs)
                instance = sorted(qs, key=lambda item: ids.index(item.id))

        return super().many_init(instance, *args, **kwargs)

    @classmethod
    def setup_eager_loading(cls, queryset):

        if cls.select_related:
            queryset = queryset.select_related(*cls.select_related)

        if cls.prefetch_related:
            queryset = queryset.prefetch_related(*cls.prefetch_related)

        if cls.annotate:
            queryset = queryset.annotate(**cls.annotate)

        if cls.aggregate:
            queryset = queryset.aggregate(**cls.aggregate)

        return queryset
