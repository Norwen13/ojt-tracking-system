from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .decorators import admin_login_required
from .forms import (
    LoginForm, SchoolAdminForm, StudentForm, CompanyForm, CoordinatorForm,
    OJTPlacementForm, AttendanceForm,
)
from .models import SchoolAdmin, Student, Company, Coordinator, OJTPlacement, Attendance


class AdminRequiredMixin:
    """Applies the custom (non-Django-admin) session login guard to CBVs."""

    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return method_decorator(admin_login_required)(view)


# ---------------------------------------------------------------------------
# Authentication (custom, session-based - NOT django.contrib.admin)
# ---------------------------------------------------------------------------

def login_view(request):
    if request.session.get(settings.ADMIN_SESSION_KEY):
        return redirect("dashboard")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        admin_id = form.cleaned_data["admin_id"]
        password = form.cleaned_data["password"]
        try:
            admin = SchoolAdmin.objects.get(pk=admin_id)
        except SchoolAdmin.DoesNotExist:
            admin = None

        if admin and admin.check_password(password):
            request.session[settings.ADMIN_SESSION_KEY] = admin.admin_id
            messages.success(request, "Welcome back!")
            return redirect("dashboard")
        messages.error(request, "Invalid admin ID or password.")

    return render(request, "placement/login.html", {"form": form})


def logout_view(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect("login")


@method_decorator(admin_login_required, name="dispatch")
class DashboardView(View):
    def get(self, request):
        counts = {
            "students": Student.objects.count(),
            "companies": Company.objects.count(),
            "coordinators": Coordinator.objects.count(),
            "placements": OJTPlacement.objects.count(),
            "attendance": Attendance.objects.count(),
            "admins": SchoolAdmin.objects.count(),
        }
        return render(request, "placement/dashboard.html", {"counts": counts})
