from django.db import models
from users.models import MyUser
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from friends.forms import UserFriendsRoleForm
# Create your models here.


class Friends(models.Model):
    nickname = models.CharField(max_length=30)

    def __str__(self):
        return self.nickname

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

    # Utworzyc pomocnicza klase i przeniesc metode, rozbic metode
    @staticmethod
    def update_members(count: int, post_data: dict):
        members_count = count
        for it in range(0, members_count):
            member_data = UserToFriends.from_formset_data(post_data, it)
            try:
                member = UserToFriends.objects.get(pk=member_data.get('id'))
            except ObjectDoesNotExist:
                pass
            else:
                if not member.owner:
                    member.admin = member_data.get('admin')
                    member.owner = member_data.get('owner')
                    member.save()


class JoinRequest(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    friends = models.ForeignKey(Friends, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} request joining {self.friends.nickname}"
