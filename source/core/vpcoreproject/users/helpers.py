from django.forms import ModelForm


def get_modelform_data_from_post(post: dict, form: type(ModelForm)) -> dict:
    return_dict = {}
    temp_form_instance = form()
    for field in temp_form_instance.fields:
        if field in post.keys():
            return_dict[field] = post.get(field, None)
    return return_dict
