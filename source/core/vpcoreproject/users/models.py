from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


class FamilySize(models.Model):
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    infants = models.IntegerField(default=0)

    def __str__(self):
        return (
            f"Adults: {self.adults}, children: {self.children}, infants: {self.infants}"
        )


class MyUser(AbstractUser):
    default_family = models.OneToOneField(
        FamilySize, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.username


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
