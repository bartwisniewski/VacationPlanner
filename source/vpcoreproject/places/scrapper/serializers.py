from rest_framework import serializers

from webscrapper.schemas.schemas import Query, Place


class QuerySerializer(serializers.Serializer):
    region = serializers.CharField(default="")
    adults = serializers.IntegerField(default=1)
    children = serializers.IntegerField(default=0)
    infants = serializers.IntegerField(default=0)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    def create(self, validated_data):
        return Query(**validated_data)


class PlaceSerializer(serializers.Serializer):
    name = serializers.CharField(default="")
    url = serializers.URLField(default="")
    description = serializers.CharField(default="")
    address = serializers.CharField(default="")
    city = serializers.CharField(default="")
    country = serializers.CharField(default="")
    region = serializers.CharField(default="")
    place_type = serializers.CharField(default="")
    owner_name = serializers.CharField(default="")
    owner_phone = serializers.CharField(default="")
    owner_email = serializers.CharField(default="")
    adults = serializers.IntegerField(default=1)
    children = serializers.IntegerField(default=0)
    infants = serializers.IntegerField(default=0)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    living_rooms = serializers.IntegerField(default=0)
    kitchens = serializers.IntegerField(default=0)
    price = serializers.FloatField(default=0.0)


class StatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.IntegerField()
