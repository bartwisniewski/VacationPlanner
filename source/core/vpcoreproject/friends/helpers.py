from django.contrib import messages


def owner_only(method):
    def inner(view, *args, **kwargs):
        if view.object.test_user_role(view.request.user, 'owner'):
            method(view, *args, **kwargs)
        else:
            messages.warning(view.request, "You are not the owner")
    return inner
