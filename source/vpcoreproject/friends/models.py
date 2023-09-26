from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.forms import formset_factory
from friends.forms import UserFriendsRoleForm
from members.models import Member
from users.models import MyUser

UserModel = get_user_model()


class Friends(models.Model):
    nickname = models.CharField(max_length=30)

    def __str__(self):
        return self.nickname

    @staticmethod
    def get_or_warning(id, request):
        try:
            return Friends.objects.get(id=id)
        except ObjectDoesNotExist:
            messages.warning(request, f"Friends group with id {id} does not exist")
        return None

    @staticmethod
    def filter_by_user(user: UserModel):
        return Friends.objects.filter(usertofriends__user=user)

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
            "form-TOTAL_FORMS": f"{count}",
            "form-INITIAL_FORMS": f"{count}",
        }
        form_id = 0
        for related_user in related_users:
            data.update(related_user.to_formset_data(form_id))
            form_id += 1
        formset_class = formset_factory(UserFriendsRoleForm)
        formset = formset_class(data)
        return formset


class UserToFriends(Member):
    friends = models.ForeignKey(Friends, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} is in {self.friends.nickname}"

    @staticmethod
    def get_or_warning(user, friends, request):
        try:
            return UserToFriends.objects.get(user=user, friends=friends)
        except ObjectDoesNotExist:
            messages.warning(request, f"User {user} is not member of {friends} group")
        return None


class JoinRequest(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    friends = models.ForeignKey(Friends, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} request joining {self.friends.nickname}"
