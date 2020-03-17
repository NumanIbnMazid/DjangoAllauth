from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .utils import unique_slug_generator, generate_time_str_num
from middlewares.middlewares import RequestMiddleware
from .choices import (
    GENDER_CHOICES, USER_ROLE_CHOICES, BLOOD_GROUP_CHOICES
)
from django.contrib.auth.models import User



class UserProfile(models.Model):
    
    # Model Fields
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE, related_name='profile', verbose_name='user'
    )
    slug = models.SlugField(
        unique=True, max_length=255, verbose_name='slug'
    )
    role = models.PositiveSmallIntegerField(
        choices=USER_ROLE_CHOICES, default=2, verbose_name='role'
    )
    gender = models.CharField(
        choices=GENDER_CHOICES, blank=True, null=True, max_length=10, verbose_name='gender'
    )
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUP_CHOICES, verbose_name='blood group'
    )
    about = models.TextField(
        max_length=300, blank=True, null=True, verbose_name='about'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='updated at'
    )

    class Meta:
        verbose_name = ("User Profile")
        verbose_name_plural = ("User Profiles")
        ordering = ["-user__date_joined"]

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username

    def get_name(self):
        name = None
        if self.user.first_name or self.user.last_name:
            name = self.user.get_full_name()
        else:
            name = self.user.username
        return name

    def get_smallname(self):
        if self.user.first_name or self.user.last_name:
            name = self.user.get_short_name()
        else:
            name = self.user.username
        return name

    def get_dynamic_name(self):
        if len(self.get_username()) < 13:
            name = self.get_username()
        else:
            name = self.get_smallname()
        return name

    def get_role(self):
        role = None
        if self.role == 0:
            role = 'Marketing Manager'
        if self.role == 1:
            role = 'Administrator'
        if self.role == 2:
            role = 'Site Guest'
        return role

    def get_fields(self):
        def get_dynamic_fields(field):
            if field.name == 'x':
                return (field.name, self.x.title)
            else:
                return (field.name, field.value_from_object(self))
        return [get_dynamic_fields(field) for field in self.__class__._meta.fields]


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    username = instance.username.lower()
    slug_binding = username+'-'+generate_time_str_num()
    try:
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        blood_group = request.POST.get("blood_group")
        gender = request.POST.get("gender")
        role = request.POST.get("role")
        if not role == None:
            if created:
                UserProfile.objects.create(
                    user=instance, blood_group=blood_group, role=role, gender=gender, slug=slug_binding)
        else:
            if created:
                UserProfile.objects.create(
                    user=instance, blood_group=blood_group, slug=slug_binding)
    except AttributeError:
        if created:
            UserProfile.objects.create(
                user=instance, slug=slug_binding)
    instance.profile.save()

