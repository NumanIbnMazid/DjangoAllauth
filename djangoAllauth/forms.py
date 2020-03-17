from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from accounts.choices import BLOOD_GROUP_CHOICES, USER_ROLE_CHOICES
from middlewares.middlewares import RequestMiddleware


class CustomSignupForm(SignupForm):
    NONE = ''
    A_POSITIVE = 'A+'
    A_NEGATIVE = 'A-'
    B_POSITIVE = 'B+'
    B_NEGATIVE = 'B-'
    O_POSITIVE = 'O+'
    O_NEGATIVE = 'O-'
    AB_POSITIVE = 'AB+'
    AB_NEGATIVE = 'AB-'
    BLOOD_GROUP_CHOICES = (
        (NONE, '--- Select Blood Group ---'),
        (A_POSITIVE, 'A+'),
        (A_NEGATIVE, 'A-'),
        (B_POSITIVE, 'B+'),
        (B_NEGATIVE, 'B-'),
        (O_POSITIVE, 'O+'),
        (O_NEGATIVE, 'O-'),
        (AB_POSITIVE, 'AB+'),
        (AB_NEGATIVE, 'AB-')
    )

    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUP_CHOICES, label="Blood Group", initial='',
         widget=forms.Select(), required=True)
    # request = RequestMiddleware(get_response=None)
    # request = request.thread_local.current_request
    # if request.user.is_superuser:
    #     role = forms.ChoiceField(
    #         choices=USER_ROLE_CHOICES, label="User Role", initial='',
    #         widget=forms.Select(), required=True)

    def signup(self, request, user):
        user.save()
        userprofile, created = self.get_or_create(user=user)
        user.userprofile.save()
