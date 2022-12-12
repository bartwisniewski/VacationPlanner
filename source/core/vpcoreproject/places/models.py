from django.db import models
from django.db.models import SET_NULL
from django.utils.translation import gettext_lazy as _
from users.models import FamilySize
from django.contrib.auth import get_user_model

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
        HOTEL = 'HT', _('Hotel')
        HOUSE = 'HS', _('House')
        BUNGALOW = 'BG', _('Bungalow')
        FLAT = 'FL', _('Flat')
        AGRITOURISM = 'AG', _('Agritourism')
        CAMPING = 'CA', _('Camping')
        YACHT = 'YA', _('Yacht')

    class PlaceRegion(models.TextChoices):
        MOUNTAINS = 'MT', _('Mountains')
        LAKE = 'LK', _('Lake')
        SEA = 'SE', _('Sea')
        WOOD = 'WD', _('Wood')
        FIELDS = 'FL', _('Fields')
        CITY = 'CT', _('City')

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
