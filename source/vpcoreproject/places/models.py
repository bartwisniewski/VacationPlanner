from django.db import models
from django.db.models import SET_NULL, Q, F
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import get_user_model

from users.models import FamilySize


UserModel = get_user_model()


class Owner(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name}"


class PlaceSize(models.Model):
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    living_rooms = models.IntegerField(default=0)
    kitchens = models.IntegerField(default=0)

    def __str__(self):
        return f"bd:{self.bedrooms}-bt:{self.bathrooms}-lv:{self.living_rooms}-kt:{self.kitchens}"


class Place(models.Model):
    class PlaceTypes(models.TextChoices):
        HOTEL = "HT", _("Hotel")
        HOUSE = "HS", _("House")
        BUNGALOW = "BG", _("Bungalow")
        FLAT = "FL", _("Flat")
        AGRITOURISM = "AG", _("Agritourism")
        CAMPING = "CA", _("Camping")
        YACHT = "YA", _("Yacht")

    class PlaceRegion(models.TextChoices):
        MOUNTAINS = "MT", _("Mountains")
        LAKE = "LK", _("Lake")
        SEA = "SE", _("Sea")
        WOOD = "WD", _("Wood")
        FIELDS = "FL", _("Fields")
        CITY = "CT", _("City")

    name = models.CharField(max_length=30)
    url = models.URLField()
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=30)
    owner = models.ForeignKey(Owner, on_delete=SET_NULL, null=True)
    capacity = models.OneToOneField(FamilySize, on_delete=models.SET_NULL, null=True)
    size = models.OneToOneField(PlaceSize, on_delete=models.SET_NULL, null=True)
    type = models.CharField(
        max_length=2,
        choices=PlaceTypes.choices,
        default=PlaceTypes.HOTEL,
    )
    region = models.CharField(
        max_length=2,
        choices=PlaceRegion.choices,
        default=PlaceRegion.MOUNTAINS,
    )
    created_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def user_places(user: UserModel):
        return Place.objects.filter(created_by=user)

    def delete(self, *args, **kwargs):
        self.owner.delete(*args, **kwargs)
        self.capacity.delete(*args, **kwargs)
        self.size.delete(*args, **kwargs)
        super().delete(*args, **kwargs)

    @staticmethod
    def filter_char(field: models.Field, filter_phrase: str):
        model_field = field.field
        field_name = model_field.name
        choices = model_field.choices
        if choices:
            return Place.filter_char_choice(field_name, choices, filter_phrase)
        field_name_icontains = field_name + "__icontains"
        return Q(**{field_name_icontains: filter_phrase})

    @staticmethod
    def filter_char_choice(field_name: str, choices: list, filter_phrase: str):
        found_choices = [choice[0] for choice in choices if choice[1] == filter_phrase]
        field_name_in = field_name + "__in"
        return Q(**{field_name_in: found_choices})

    @staticmethod
    def compile_filter(filter_phrase: str):
        compiled_filter = Place.filter_char(Place.name, filter_phrase)
        compiled_filter |= Place.filter_char(Place.description, filter_phrase)
        compiled_filter |= Place.filter_char(Place.country, filter_phrase)
        compiled_filter |= Place.filter_char(Place.city, filter_phrase)
        compiled_filter |= Place.filter_char(Place.region, filter_phrase)
        compiled_filter |= Place.filter_char(Place.type, filter_phrase)
        return compiled_filter

    @staticmethod
    def add_filter_by_capacity(queryset, max_capacity: FamilySize) -> Q:
        queryset = queryset.annotate(
            capacity_total=F("capacity__adults") + F("capacity__children")
        )
        total = max_capacity.total
        compiled_filter = Q(capacity__isnull=True) | Q(
            capacity__adults__gte=max_capacity.adults, capacity_total__gte=total
        )
        return queryset.filter(compiled_filter)


class PlaceScrap(models.Model):
    class ScrapStatus(models.IntegerChoices):
        PENDING = 0, _("PENDING")
        SUCCESS = 3, _("SUCCESS")
        FAILURE = 4, _("FAILURE")

    task_id = models.CharField(max_length=40)
    status = models.IntegerField(
        choices=ScrapStatus.choices, default=ScrapStatus.PENDING
    )
    created_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)

    @staticmethod
    def user_scraps(user: UserModel):
        return PlaceScrap.objects.filter(created_by=user)

    @staticmethod
    def get_or_warning(task_id, request):
        try:
            return PlaceScrap.objects.get(task_id=task_id)
        except ObjectDoesNotExist:
            messages.warning(
                request, f"Scrapping job with task_id {task_id} does not exist"
            )
        return None
