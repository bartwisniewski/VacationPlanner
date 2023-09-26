from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Create your models here.


class FamilySize(models.Model):
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    infants = models.IntegerField(default=0)

    def __str__(self):
        return (
            f"Adults: {self.adults}, children: {self.children}, infants: {self.infants}"
        )

    @property
    def total(self):
        return self.adults + self.children

    @total.setter
    def total(self, val):
        pass

    def __add__(self, obj2):
        adults = self.adults + obj2.adults
        children = self.children + obj2.children
        infants = self.infants + obj2.infants
        return FamilySize(adults=adults, children=children, infants=infants)

    def __eq__(self, obj2):
        return self.adults == obj2.adults and self.children == obj2.children

    def __lt__(self, obj2):
        return self.adults < obj2.adults or self.total < obj2.total

    def __le__(self, obj2):
        return self.adults <= obj2.adults or self.total <= obj2.total

    def __gt__(self, obj2):
        return self.adults > obj2.adults and self.total > obj2.total

    def __ge__(self, obj2):
        return self.adults >= obj2.adults and self.total >= obj2.total


class MyUser(AbstractUser):
    default_family = models.OneToOneField(
        FamilySize, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.username

    def get_default_family(self):
        try:
            return self.default_family
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_by_name_or_none(username):
        try:
            return MyUser.objects.get(username=username)
        except ObjectDoesNotExist:
            pass
        return None


class SocialMedia(models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField()

    def __str__(self):
        return self.name


class SocialUser(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    social_name = models.CharField(max_length=50)
    social_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} on {self.social_media.name} is {self.social_name}"
