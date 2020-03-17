from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, CreateView, ListView
from .models import UserProfile
from django.contrib import messages
from .forms import UserProfileForm
from django.urls import reverse
# from djangoAllauth.forms import CustomSignupForm
from .forms import UserForm, BaseUserForm, AdminUserProfileForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Custom Decorators Starts
from accounts.decorators import (
    is_superuser_required
)
# Custom Decorators Ends

decorators = [login_required, is_superuser_required]


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    template_name = 'profile/profile-details.html'

    def get_object(self):
        qs = UserProfile.objects.filter(slug=self.kwargs['slug'])
        if qs.exists():
            return qs.first()
        return None


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    template_name = 'profile/profile-update.html'
    form_class = UserProfileForm

    def get_object(self):
        qs = UserProfile.objects.filter(slug=self.kwargs['slug'])
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        self.object = self.get_object()
        messages.add_message(self.request, messages.SUCCESS,
                             "Your profile has been updated successfully !")
        return super().form_valid(form)

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse('profile_update', kwargs={'slug': slug})


@method_decorator(decorators, name='dispatch')
class UserCreateView(CreateView):
    template_name = 'snippets/manage.html'
    form_class = BaseUserForm


    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')
        email_qs = User.objects.filter(
            email__iexact=email
        )
        if email_qs.exists():
            form.add_error(
                'email', forms.ValidationError(
                    "This email is already registered ! Please try another one."
                )
            )
            return super().form_invalid(form)
        messages.add_message(
            self.request, messages.SUCCESS,
            "User created successfully!"
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('add_user')




class UserProfileListView(ListView):
    template_name = 'profile/profile-list.html'

    def get_queryset(self):
        query = UserProfile.objects.all()
        return query


class UserProfileAdminUpdateView(UpdateView):
    template_name = 'snippets/manage.html'
    form_class = AdminUserProfileForm

    def get_object(self):
        slug = self.kwargs['slug']
        qs = UserProfile.objects.filter(
            slug=slug
        )
        if qs.exists():
            return qs.first()
        return None

    def form_valid(self, form):
        # pre = self.get_object()
        # email = form.cleaned_data.get('email')
        # username = form.cleaned_data.get('username')
        
        # if not pre.email == email:
        #     email_qs = User.objects.filter(
        #         email__iexact=email
        #     )
        #     if email_qs.exists():
        #         form.add_error(
        #             'email', forms.ValidationError(
        #                 "This email is already registered ! Please try another one."
        #             )
        #         )
        #         return super().form_invalid(form)
        # if not pre.username == username:
        #     username_qs = User.objects.filter(
        #         username__iexact=username
        #     )
        #     if username_qs.exists():
        #         form.add_error(
        #             'username', forms.ValidationError(
        #                 "This username is already registered ! Please try another one."
        #             )
        #         )
        #         return super().form_invalid(form)
        messages.add_message(
            self.request, messages.SUCCESS,
            "User updated successfully!"
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile_list')
