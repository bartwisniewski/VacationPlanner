from django.db.models import Model
from datetime import date, datetime


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


def date_2_datetime(in_date: date) -> datetime:
    return datetime(in_date.year, in_date.month, in_date.day)
