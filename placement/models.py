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
