from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.DashboardView.as_view(), name="dashboard"),

    # School Admin accounts
    path("admins/", views.SchoolAdminListView.as_view(), name="schooladmin_list"),
    path("admins/add/", views.SchoolAdminCreateView.as_view(), name="schooladmin_create"),
    path("admins/<int:pk>/edit/", views.SchoolAdminUpdateView.as_view(), name="schooladmin_update"),
    path("admins/<int:pk>/delete/", views.SchoolAdminDeleteView.as_view(), name="schooladmin_delete"),

    # Students
    path("students/", views.StudentListView.as_view(), name="student_list"),
    path("students/add/", views.StudentCreateView.as_view(), name="student_create"),
    path("students/<int:pk>/edit/", views.StudentUpdateView.as_view(), name="student_update"),
    path("students/<int:pk>/delete/", views.StudentDeleteView.as_view(), name="student_delete"),

    # Companies
    path("companies/", views.CompanyListView.as_view(), name="company_list"),
    path("companies/add/", views.CompanyCreateView.as_view(), name="company_create"),
    path("companies/<int:pk>/edit/", views.CompanyUpdateView.as_view(), name="company_update"),
    path("companies/<int:pk>/delete/", views.CompanyDeleteView.as_view(), name="company_delete"),

    # Coordinators
    path("coordinators/", views.CoordinatorListView.as_view(), name="coordinator_list"),
    path("coordinators/add/", views.CoordinatorCreateView.as_view(), name="coordinator_create"),
    path("coordinators/<int:pk>/edit/", views.CoordinatorUpdateView.as_view(), name="coordinator_update"),
    path("coordinators/<int:pk>/delete/", views.CoordinatorDeleteView.as_view(), name="coordinator_delete"),

    # OJT Placements
    path("placements/", views.OJTPlacementListView.as_view(), name="placement_list"),
    path("placements/add/", views.OJTPlacementCreateView.as_view(), name="placement_create"),
    path("placements/<int:pk>/edit/", views.OJTPlacementUpdateView.as_view(), name="placement_update"),
    path("placements/<int:pk>/delete/", views.OJTPlacementDeleteView.as_view(), name="placement_delete"),

    # Attendance
    path("attendance/", views.AttendanceListView.as_view(), name="attendance_list"),
    path("attendance/add/", views.AttendanceCreateView.as_view(), name="attendance_create"),
    path("attendance/<int:pk>/edit/", views.AttendanceUpdateView.as_view(), name="attendance_update"),
    path("attendance/<int:pk>/delete/", views.AttendanceDeleteView.as_view(), name="attendance_delete"),
]
