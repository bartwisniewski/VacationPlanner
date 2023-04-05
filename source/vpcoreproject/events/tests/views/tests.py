from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.urls import reverse
from events.models import Event, UserToEvent

client = Client()
