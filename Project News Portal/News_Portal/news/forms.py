from django.forms import ModelForm

from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from pytz import common_timezones
from django import forms


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'author', 'category', 'text', 'post_type']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


class TimezoneForm(forms.Form):
    timezone = forms.ChoiceField(choices=[(tz, tz) for tz in common_timezones])
