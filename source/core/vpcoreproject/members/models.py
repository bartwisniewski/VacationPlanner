from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

UserModel = get_user_model()


class Member(models.Model):
    UserModel = get_user_model()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)
    owner = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.username}"

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
