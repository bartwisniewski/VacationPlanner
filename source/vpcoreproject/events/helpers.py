from django.db.models import Model, Q
from events.models import UserToEvent
from members.helpers import MembersUpdateManager


class UserToEventUpdateManager(MembersUpdateManager):
    Model = UserToEvent


def filter_from_field(field_name: str, filter_phrase: str):
    field_name_icontains = field_name + "__icontains"
    return Q(**{field_name_icontains: filter_phrase})


def compile_filter(fields: list, filter_phrase: str):
    if not fields:
        return None
    compiled_filter = filter_from_field(fields[0], filter_phrase)
    for field in fields[1:]:
        compiled_filter = compiled_filter | filter_from_field(field, filter_phrase)
    return compiled_filter


def get_field_value_from_related_object(
    instance: Model, relation_field: str, field_name: str
):
    if not instance:
        return None
    related_object = getattr(instance, relation_field)
    if not related_object:
        return None
    related_object_field_value = getattr(related_object, field_name)
    return related_object_field_value
