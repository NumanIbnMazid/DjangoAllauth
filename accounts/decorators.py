from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings


# SUper Admin Required

is_superuser_required = user_passes_test(
    lambda user: user.is_superuser == True, login_url=settings.HOME_URL)


def can_browse_required(view_func):
    decorated_view_func = login_required(is_superuser_required(view_func))
    return decorated_view_func
