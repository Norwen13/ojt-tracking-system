from functools import wraps

from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages


def admin_login_required(view_func):
    """
    Custom session-based auth guard (NOT django.contrib.admin).
    Requires a School Admin to be logged in (see views.login_view) before
    accessing any data-management interface.
    """

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get(settings.ADMIN_SESSION_KEY):
            messages.warning(request, "Please log in to continue.")
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return _wrapped
