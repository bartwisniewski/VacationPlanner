from django.db import models
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory

from users.models import MyUser
from friends.forms import UserFriendsRoleForm
# Create your models here.


class Friends(models.Model):
    nickname = models.CharField(max_length=30)

    def __str__(self):
        return self.nickname

    @staticmethod
    def get_or_warning(id, request):
        try:
            return Friends.objects.get(id=id)
        except ObjectDoesNotExist:
            messages.warning(request, f'Friends group with id {id} does not exist')
        return None

    def test_user_role(self, user, role):
        try:
            relation = self.usertofriends_set.get(user=user)
        except ObjectDoesNotExist:
            return False
        return getattr(relation, role, False)

    def get_users_formset(self):
        related_users = self.usertofriends_set.all()
        count = related_users.count()
        data = {
        'form-TOTAL_FORMS': f'{count}',
        'form-INITIAL_FORMS': f'{count}',
        }
        form_id = 0
        for related_user in related_users:
            data.update(related_user.to_formset_data(form_id))
            form_id += 1
        formset_class = formset_factory(UserFriendsRoleForm)
        formset = formset_class(data)
        return formset


class UserToFriends(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    friends = models.ForeignKey(Friends, on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)
    owner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} is in {self.friends.nickname}"

    @staticmethod
    def get_or_warning(user, friends, request):
        try:
            return UserToFriends.objects.get(user=user, friends=friends)
        except ObjectDoesNotExist:
            messages.warning(request, f'User {user} does not belong to {friends}')
        return None

    def to_formset_data(self, form_id: int) -> dict:
        formset_data = {f'form-{form_id}-id': self.id,
                        f'form-{form_id}-username': self.user.username,
                        f'form-{form_id}-admin': self.admin,
                        f'form-{form_id}-owner': self.owner}
        return formset_data

    @staticmethod
    def from_formset_data(data: dict, form_id: int) -> dict:
        fields = [('id', None), ('username', ''), ('admin', False), ('owner', False)]
        object_data = {}
        for field in fields:
            object_data[field[0]] = data.get(f'form-{form_id}-{field[0]}', field[1])
            if object_data[field[0]] == 'on':
                object_data[field[0]] = True
        return object_data


class JoinRequest(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    friends = models.ForeignKey(Friends, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} request joining {self.friends.nickname}"
