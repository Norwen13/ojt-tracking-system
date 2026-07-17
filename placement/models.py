from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class SchoolAdmin(models.Model):
    """
    SCHOOL ADMIN entity from the ERD.
    Fields: admin_id (PK), password.
    The School Admin account manages Company and Coordinator accounts
    ("Handles" relationships on the ERD) through the custom interface.
    """

    admin_id = models.CharField(max_length=50, primary_key=True)
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


class OJTPlacement(models.Model):
    """
    OJT_PLACEMENT entity from the ERD.
    Fields: placement_id (PK), student_id (FK), company_id (FK),
    coordinator_id (FK), start_date, end_date, required_hours, status.

    Relationships (matches the ERD crow's-foot notation):
      - Student (1) --- (0..many) OJT_PLACEMENT
      - Company (1) --- (0..many) OJT_PLACEMENT   ("host")
      - Coordinator (1) --- (0..many) OJT_PLACEMENT  ("supervises")
      - OJT_PLACEMENT (1) --- (0..many) ATTENDANCE  ("generates")
    """

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Ongoing", "Ongoing"),
        ("Completed", "Completed"),
        ("Terminated", "Terminated"),
    ]

    placement_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="placements", db_column="student_id"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="placements", db_column="company_id"
    )
    coordinator = models.ForeignKey(
        Coordinator, on_delete=models.CASCADE, related_name="placements", db_column="coordinator_id"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    required_hours = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    class Meta:
        verbose_name = "OJT Placement"
        verbose_name_plural = "OJT Placements"
        ordering = ["-start_date"]

    def __str__(self):
        return f"Placement #{self.placement_id}: {self.student} @ {self.company}"

    @property
    def total_rendered_hours(self):
        total = self.attendance_logs.aggregate(total=models.Sum("rendered_hours"))["total"]
        return round(total or 0, 2)

    @property
    def hours_remaining(self):
        return max(round(self.required_hours - self.total_rendered_hours, 2), 0)

    @property
    def progress_percent(self):
        if not self.required_hours:
            return 0
        return min(round((self.total_rendered_hours / self.required_hours) * 100), 100)


class Attendance(models.Model):
    """
    ATTENDANCE entity from the ERD.
    Fields: attendance_id (PK), placement_id (FK), log_date, time_in,
    time_out, rendered_hours, status, remarks.
    Relationship: one OJT_PLACEMENT "generates" many ATTENDANCE records.
    """

    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Late", "Late"),
        ("Excused", "Excused"),
    ]

    attendance_id = models.AutoField(primary_key=True)
    placement = models.ForeignKey(
        OJTPlacement, on_delete=models.CASCADE, related_name="attendance_logs", db_column="placement_id"
    )
    log_date = models.DateField()
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    rendered_hours = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Present")
    remarks = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance Records"
        ordering = ["-log_date"]

    def __str__(self):
        return f"Attendance #{self.attendance_id} - {self.log_date}"

def _student_active_placement(self):
    """Returns the student's current Ongoing placement, or their most recent one."""
    return (
        self.placements.filter(status="Ongoing").order_by("-start_date").first()
        or self.placements.order_by("-start_date").first()
    )


Student.active_placement = property(_student_active_placement)
