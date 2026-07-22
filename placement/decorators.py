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
        # Guard against a stale student session lingering in the same
        # browser session from before this fix (or a shared/switched login).
        request.session.pop(settings.STUDENT_SESSION_KEY, None)
        return view_func(request, *args, **kwargs)

    return _wrapped

def student_login_required(view_func):
    """
    Custom session-based auth guard for the Student Portal.
    Requires a Student to be logged in (see views.student_login_view) before
    accessing any student-facing page.
    """

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get(settings.STUDENT_SESSION_KEY):
            messages.warning(request, "Please log in to continue.")
            return redirect("student_login")
        # Guard against a stale admin session lingering in the same
        # browser session from before this fix (or a shared/switched login).
        request.session.pop(settings.ADMIN_SESSION_KEY, None)
        return view_func(request, *args, **kwargs)

    return _wrapped