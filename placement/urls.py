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
]
