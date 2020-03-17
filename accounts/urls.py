from django.urls import path, include
from .views import (
    ProfileDetailView, ProfileUpdateView, UserCreateView, UserProfileListView,
    UserProfileAdminUpdateView
)

urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/<slug>/view/',
         ProfileDetailView.as_view(), name='profile_details'),
    path('profile/<slug>/update/',
         ProfileUpdateView.as_view(), name='profile_update'),
    path('user/profile/list/',
         UserProfileListView.as_view(), name='profile_list'),
    path('add/user/',
         UserCreateView.as_view(), name='add_user'),
    path('update/user/<slug>/',
         UserProfileAdminUpdateView.as_view(), name='update_user'),
]
