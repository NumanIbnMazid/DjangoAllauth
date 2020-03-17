from django.contrib import admin
from .mixing import CustomModelAdminMixin

from .models import (
    UserProfile
)


class UserProfileAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = UserProfile


admin.site.register(UserProfile, UserProfileAdmin)
