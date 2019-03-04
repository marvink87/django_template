from django import forms
from django.apps import apps


def get_default_form(model_instance):
    conditional_model = model_instance

    class DefaultForm(forms.ModelForm):
        class Meta:
            model = conditional_model
            exclude = ('pk',)

    return DefaultForm
