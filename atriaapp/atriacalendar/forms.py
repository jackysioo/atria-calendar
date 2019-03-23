from django import forms
from modeltranslation.forms import TranslationModelForm
from django.contrib.auth.forms import UserCreationForm

from swingtime import models as swingtime_models
from swingtime import forms as swingtime_forms

from .models import *


# class EventForm(TranslationModelForm):
#    """
#    A simple form for adding and updating Event attributes.
#    """
#
#    class Meta:
#        model = Event
#        fields = "__all__"
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields['description'].required = False

class AtriaEventForm(swingtime_forms.EventForm, TranslationModelForm):
    """
    A simple form for adding and updating Event attributes.
    """

    class Meta:
        model = AtriaEvent
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['program'].required = False
        # self.fields['location'].required = False


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Optional.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    def save(self):
        user = super().save()
        if Group.objects.filter(name='Attendee').exists():
            user.groups.add(Group.objects.get(name='Attendee'))

        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class OrgSignUpForm(SignUpForm):
    org_name = forms.CharField(max_length=40, required=True,
                                 help_text='Required.')
    description = forms.CharField(max_length=4000, required=True,
                                 help_text='Required.', widget=forms.Textarea)
    location = forms.CharField(max_length=80, required=True,
                                 help_text='Required.')

    def save(self):
        user = super(OrgSignUpForm, self).save()
        if Group.objects.filter(name='Admin').exists():
            user.groups.add(Group.objects.get(name='Admin'))

        return user

