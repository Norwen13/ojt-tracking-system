from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class SchoolAdmin(models.Model):
    """
    SCHOOL ADMIN entity from the ERD.
    Fields: admin_id (PK), password.
    The School Admin account manages Company and Coordinator accounts
    ("Handles" relationships on the ERD) through the custom interface.
    """

    admin_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)

    class Meta:
        verbose_name = "School Admin"
        verbose_name_plural = "School Admins"
        ordering = ["admin_id"]

    def __str__(self):
        return f"Admin #{self.admin_id}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Company(models.Model):
    """
    COMPANY entity from the ERD.
    Fields: company_id (PK), company_name, contact_person, password,
    industry_type, contact_number, email.
    Relationship: one Company can "host" many OJT_PLACEMENT records.
    A School Admin "handles" (manages) Company accounts.
    """

    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    industry_type = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["company_name"]

    def __str__(self):
        return f"{self.company_name} ({self.company_id})"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Coordinator(models.Model):
    """
    COORDINATOR entity from the ERD.
    Fields: coordinator_id (PK), first_name, last_name, password, email,
    department.
    Relationship: one Coordinator "supervises" many OJT_PLACEMENT records.
    A School Admin "handles" (manages) Coordinator accounts.
    """

    coordinator_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=150, unique=True)
    department = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Coordinator"
        verbose_name_plural = "Coordinators"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.coordinator_id})"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Student(models.Model):
    """
    STUDENT entity from the ERD.
    Fields: student_id (PK), first_name, last_name, email, contact_number,
    password, course, department, year_level, section, required_hours.
    Relationship: one Student can be linked to many OJT_PLACEMENT records.
    """

    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    contact_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    course = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    year_level = models.PositiveSmallIntegerField()
    section = models.CharField(max_length=20)
    required_hours = models.PositiveIntegerField(help_text="Total OJT hours required for this student")

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.student_id})"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
