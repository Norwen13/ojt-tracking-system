from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .decorators import student_login_required
from .forms import StudentLoginForm


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
        return admin_login_required(view)


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
            request.session.pop(settings.STUDENT_SESSION_KEY, None)
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


# ---------------------------------------------------------------------------
# SCHOOL ADMIN - custom CRUD interface (account management)
# ---------------------------------------------------------------------------

class SchoolAdminListView(AdminRequiredMixin, ListView):
    model = SchoolAdmin
    template_name = "placement/generic_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "entity_name": "Admin Account",
            "entity_name_plural": "School Admin Accounts",
            "headers": ["Admin ID"],
            "fields": ["admin_id"],
            "create_url_name": "schooladmin_create",
            "update_url_name": "schooladmin_update",
            "delete_url_name": "schooladmin_delete",
        })
        return context


class SchoolAdminCreateView(AdminRequiredMixin, CreateView):
    model = SchoolAdmin
    form_class = SchoolAdminForm
    template_name = "placement/generic_form.html"
    success_url = reverse_lazy("schooladmin_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"form_title": "Add School Admin", "list_url_name": "schooladmin_list"})
        return context

    def form_valid(self, form):
        messages.success(self.request, "Admin account created.")
        return super().form_valid(form)


class SchoolAdminUpdateView(AdminRequiredMixin, UpdateView):
    model = SchoolAdmin
    form_class = SchoolAdminForm
    template_name = "placement/generic_form.html"
    success_url = reverse_lazy("schooladmin_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"form_title": "Edit School Admin", "list_url_name": "schooladmin_list"})
        return context

    def form_valid(self, form):
        messages.success(self.request, "Admin account updated.")
        return super().form_valid(form)


class SchoolAdminDeleteView(AdminRequiredMixin, DeleteView):
    model = SchoolAdmin
    template_name = "placement/generic_confirm_delete.html"
    success_url = reverse_lazy("schooladmin_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"entity_name": "Admin Account", "list_url_name": "schooladmin_list"})
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Admin account deleted.")
        return super().delete(request, *args, **kwargs)


# ---------------------------------------------------------------------------
# STUDENT - custom CRUD interface
# ---------------------------------------------------------------------------

class StudentListView(AdminRequiredMixin, ListView):
    model = Student
    template_name = "placement/generic_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "entity_name": "Student",
            "entity_name_plural": "Students",
            "headers": ["ID", "First Name", "Last Name", "Email", "Contact #",
                        "Course", "Department", "Year", "Section", "Required Hrs"],
            "fields": ["student_id", "first_name", "last_name", "email", "contact_number",
                       "course", "department", "year_level", "section", "required_hours"],
            "create_url_name": "student_create",
            "update_url_name": "student_update",
            "delete_url_name": "student_delete",
        })
        return context


class StudentCreateView(AdminRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "placement/generic_form.html"
    success_url = reverse_lazy("student_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"form_title": "Add Student", "list_url_name": "student_list"})
        return context

    def form_valid(self, form):
        messages.success(self.request, "Student created successfully.")
        return super().form_valid(form)


class StudentUpdateView(AdminRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "placement/generic_form.html"
    success_url = reverse_lazy("student_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"form_title": "Edit Student", "list_url_name": "student_list"})
        return context

    def form_valid(self, form):
        messages.success(self.request, "Student updated successfully.")
        return super().form_valid(form)


class StudentDeleteView(AdminRequiredMixin, DeleteView):
    model = Student
    template_name = "placement/generic_confirm_delete.html"
    success_url = reverse_lazy("student_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"entity_name": "Student", "list_url_name": "student_list"})
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Student deleted.")
        return super().delete(request, *args, **kwargs)


# ---------------------------------------------------------------------------
# COMPANY - custom CRUD interface
# ---------------------------------------------------------------------------

class CompanyListView(AdminRequiredMixin, ListView):
    model = Company
    template_name = "placement/generic_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "entity_name": "Company",
            "entity_name_plural": "Companies",
            "headers": ["ID", "Company Name", "Contact Person", "Industry Type", "Contact #", "Email"],
            "fields": ["company_id", "company_name", "contact_person", "industry_type",
                       "contact_number", "email"],
            "create_url_name": "company_create",
            "update_url_name": "company_update",
            "delete_url_name": "company_delete",
        })
        return context


class CompanyCreateView(AdminRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "placement/generic_form.html"
    success_url = reverse_lazy("company_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"form_title": "Add Company", "list_url_name": "company_list"})
        return context

    def form_valid(self, form):
        messages.success(self.request, "Company created successfully.")
        return super().form_valid(form)


class CompanyUpdateView(AdminRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "placement/generic_form.html"
    success_url = reverse_lazy("company_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"form_title": "Edit Company", "list_url_name": "company_list"})
        return context

    def form_valid(self, form):
        messages.success(self.request, "Company updated successfully.")
        return super().form_valid(form)


class CompanyDeleteView(AdminRequiredMixin, DeleteView):
    model = Company
    template_name = "placement/generic_confirm_delete.html"
    success_url = reverse_lazy("company_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"entity_name": "Company", "list_url_name": "company_list"})
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Company deleted.")
        return super().delete(request, *args, **kwargs)


# ---------------------------------------------------------------------------
# COORDINATOR - custom CRUD interface
# ---------------------------------------------------------------------------

class CoordinatorListView(AdminRequiredMixin, ListView):
    model = Coordinator
    template_name = "placement/generic_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "entity_name": "Coordinator",
            "entity_name_plural": "Coordinators",
            "headers": ["ID", "First Name", "Last Name", "Email", "Department"],
            "fields": ["coordinator_id", "first_name", "last_name", "email", "department"],
            "create_url_name": "coordinator_create",
            "update_url_name": "coordinator_update",
            "delete_url_name": "coordinator_delete",
        })
        return context


class CoordinatorCreateView(AdminRequiredMixin, CreateView):
    model = Coordinator
    form_class = CoordinatorForm
    template_name = "placement/generic_form.html"
    success_url = reverse_lazy("coordinator_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"form_title": "Add Coordinator", "list_url_name": "coordinator_list"})
        return context

    def form_valid(self, form):
        messages.success(self.request, "Coordinator created successfully.")
        return super().form_valid(form)


class CoordinatorUpdateView(AdminRequiredMixin, UpdateView):
    model = Coordinator
    form_class = CoordinatorForm
    template_name = "placement/generic_form.html"
    success_url = reverse_lazy("coordinator_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"form_title": "Edit Coordinator", "list_url_name": "coordinator_list"})
        return context

    def form_valid(self, form):
        messages.success(self.request, "Coordinator updated successfully.")
        return super().form_valid(form)


class CoordinatorDeleteView(AdminRequiredMixin, DeleteView):
    model = Coordinator
    template_name = "placement/generic_confirm_delete.html"
    success_url = reverse_lazy("coordinator_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"entity_name": "Coordinator", "list_url_name": "coordinator_list"})
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Coordinator deleted.")
        return super().delete(request, *args, **kwargs)


# ---------------------------------------------------------------------------
# OJT_PLACEMENT - custom CRUD interface (links Student, Company, Coordinator)
# ---------------------------------------------------------------------------

class OJTPlacementListView(AdminRequiredMixin, ListView):
    model = OJTPlacement
    template_name = "placement/generic_list.html"

    def get_queryset(self):
        return OJTPlacement.objects.select_related("student", "company", "coordinator")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "entity_name": "OJT Placement",
            "entity_name_plural": "OJT Placements",
            "headers": ["ID", "Student", "Company", "Coordinator", "Start Date",
                        "End Date", "Required Hrs", "Hours Rendered", "Progress %", "Status"],
            "fields": ["placement_id", "student", "company", "coordinator",
                       "start_date", "end_date", "required_hours",
                       "total_rendered_hours", "progress_percent", "status"],
            "create_url_name": "placement_create",
            "update_url_name": "placement_update",
            "delete_url_name": "placement_delete",
        })
        return context


class OJTPlacementCreateView(AdminRequiredMixin, CreateView):
    model = OJTPlacement
    form_class = OJTPlacementForm
    template_name = "placement/generic_form.html"
    success_url = reverse_lazy("placement_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"form_title": "Add OJT Placement", "list_url_name": "placement_list"})
        return context

    def form_valid(self, form):
        messages.success(self.request, "OJT Placement created successfully.")
        return super().form_valid(form)


class OJTPlacementUpdateView(AdminRequiredMixin, UpdateView):
    model = OJTPlacement
    form_class = OJTPlacementForm
    template_name = "placement/generic_form.html"
    success_url = reverse_lazy("placement_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"form_title": "Edit OJT Placement", "list_url_name": "placement_list"})
        return context

    def form_valid(self, form):
        messages.success(self.request, "OJT Placement updated successfully.")
        return super().form_valid(form)


class OJTPlacementDeleteView(AdminRequiredMixin, DeleteView):
    model = OJTPlacement
    template_name = "placement/generic_confirm_delete.html"
    success_url = reverse_lazy("placement_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"entity_name": "OJT Placement", "list_url_name": "placement_list"})
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, "OJT Placement deleted.")
        return super().delete(request, *args, **kwargs)


# ---------------------------------------------------------------------------
# ATTENDANCE - custom CRUD interface (linked to OJT_PLACEMENT)
# ---------------------------------------------------------------------------

class AttendanceListView(AdminRequiredMixin, ListView):
    model = Attendance
    template_name = "placement/generic_list.html"

    def get_queryset(self):
        return Attendance.objects.select_related("placement", "placement__student")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "entity_name": "Attendance Record",
            "entity_name_plural": "Attendance Records",
            "headers": ["ID", "Placement", "Date", "Time In", "Time Out",
                        "Rendered Hrs", "Status", "Remarks"],
            "fields": ["attendance_id", "placement", "log_date", "time_in", "time_out",
                       "rendered_hours", "status", "remarks"],
            "delete_url_name": "attendance_delete",
        })
        return context


class AttendanceCreateView(AdminRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = "placement/generic_form.html"
    success_url = reverse_lazy("attendance_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"form_title": "Add Attendance Record", "list_url_name": "attendance_list"})
        return context

    def form_valid(self, form):
        messages.success(self.request, "Attendance record created successfully.")
        return super().form_valid(form)


class AttendanceUpdateView(AdminRequiredMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = "placement/generic_form.html"
    success_url = reverse_lazy("attendance_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"form_title": "Edit Attendance Record", "list_url_name": "attendance_list"})
        return context

    def form_valid(self, form):
        messages.success(self.request, "Attendance record updated successfully.")
        return super().form_valid(form)


class AttendanceDeleteView(AdminRequiredMixin, DeleteView):
    model = Attendance
    template_name = "placement/generic_confirm_delete.html"
    success_url = reverse_lazy("attendance_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"entity_name": "Attendance Record", "list_url_name": "attendance_list"})
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Attendance record deleted.")
        return super().delete(request, *args, **kwargs)

# ---------------------------------------------------------------------------
# STUDENT PORTAL - self-service login, dashboard, and attendance clock in/out
# ---------------------------------------------------------------------------

def student_login_view(request):
    if request.session.get(settings.STUDENT_SESSION_KEY):
        return redirect("student_dashboard")

    initial = {}
    prefill_id = request.GET.get("student_id")
    if prefill_id:
        initial["student_id"] = prefill_id

    form = StudentLoginForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        student_id = form.cleaned_data["student_id"]
        password = form.cleaned_data["password"]
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            student = None

        if student and student.check_password(password):
            request.session.pop(settings.ADMIN_SESSION_KEY, None)
            request.session[settings.STUDENT_SESSION_KEY] = student.student_id
            messages.success(request, "Welcome back!")
            return redirect("student_dashboard")
        messages.error(request, "Invalid student ID or password.")

    return render(request, "placement/student_login.html", {"form": form})


def student_logout_view(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect("student_login")


@student_login_required
def student_dashboard_view(request):
    from django.utils import timezone

    student = Student.objects.get(pk=request.session[settings.STUDENT_SESSION_KEY])
    placement = student.active_placement
    today = timezone.localdate()
    today_log = None
    attendance_history = []
    if placement:
        today_log = Attendance.objects.filter(placement=placement, log_date=today).first()
        attendance_history = Attendance.objects.filter(placement=placement).order_by("-log_date")

    context = {
        "student": student,
        "placement": placement,
        "today_log": today_log,
        "attendance_history": attendance_history,
    }
    return render(request, "placement/student_dashboard.html", context)


@student_login_required
def student_clock_in_view(request):
    from django.utils import timezone

    student = Student.objects.get(pk=request.session[settings.STUDENT_SESSION_KEY])
    placement = student.active_placement

    if not placement:
        messages.error(request, "You don't have an active OJT placement yet. Contact your coordinator.")
        return redirect("student_dashboard")

    today = timezone.localdate()
    log, created = Attendance.objects.get_or_create(
        placement=placement, log_date=today,
        defaults={"time_in": timezone.localtime().time(), "status": "Present"},
    )
    if not created and log.time_in:
        messages.warning(request, "You've already clocked in today.")
    elif not created:
        log.time_in = timezone.localtime().time()
        log.status = "Present"
        log.save()
        messages.success(request, "Clocked in successfully.")
    else:
        messages.success(request, "Clocked in successfully.")

    return redirect("student_dashboard")


@student_login_required
def student_clock_out_view(request):
    from django.utils import timezone
    from datetime import datetime

    student = Student.objects.get(pk=request.session[settings.STUDENT_SESSION_KEY])
    placement = student.active_placement

    if not placement:
        messages.error(request, "You don't have an active OJT placement yet. Contact your coordinator.")
        return redirect("student_dashboard")

    today = timezone.localdate()
    try:
        log = Attendance.objects.get(placement=placement, log_date=today)
    except Attendance.DoesNotExist:
        messages.error(request, "You haven't clocked in yet today.")
        return redirect("student_dashboard")

    if not log.time_in:
        messages.error(request, "You haven't clocked in yet today.")
        return redirect("student_dashboard")

    if log.time_out:
        messages.warning(request, "You've already clocked out today.")
        return redirect("student_dashboard")

    now_time = timezone.localtime().time()
    log.time_out = now_time
    time_in_dt = datetime.combine(today, log.time_in)
    time_out_dt = datetime.combine(today, now_time)
    hours = round((time_out_dt - time_in_dt).total_seconds() / 3600, 2)
    log.rendered_hours = max(hours, 0)
    log.save()
    messages.success(request, f"Clocked out successfully. Rendered hours: {log.rendered_hours}")

    return redirect("student_dashboard")

from .forms import StudentRegisterForm


def student_register_view(request):
    if request.session.get(settings.STUDENT_SESSION_KEY):
        return redirect("student_dashboard")

    form = StudentRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        student = form.save()
        messages.success(request, f"Account created! Your Student ID is {student.student_id}. Please log in.")
        return redirect(f"/student/login/?student_id={student.student_id}")

    return render(request, "placement/student_register.html", {"form": form})