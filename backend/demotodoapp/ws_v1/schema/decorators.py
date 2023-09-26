from drf_spectacular.utils import extend_schema

from demotodoapp.ws_v1.schema.schema import ConsumerAutoSchema


def extend_ws_schema(type: str = "receive", event: str = None, **kwargs):
    def decorator(func):
        func.schema = ConsumerAutoSchema
        func.type = type
        func.event = event or func.__name__
        return extend_schema(**kwargs)(func)

    return decorator
