from django import forms

from .models import SchoolAdmin, Student, Company, Coordinator, OJTPlacement, Attendance

TEXT_WIDGET = forms.TextInput(attrs={"class": "form-control"})
PASSWORD_WIDGET = forms.PasswordInput(attrs={"class": "form-control"}, render_value=False)


class LoginForm(forms.Form):
    admin_id = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control", "autofocus": True}))
    password = forms.CharField(widget=PASSWORD_WIDGET)


class SchoolAdminForm(forms.ModelForm):
    password = forms.CharField(widget=PASSWORD_WIDGET, required=False,
                                help_text="Leave blank to keep the current password when editing.")

    class Meta:
        model = SchoolAdmin
        fields = ["password"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        raw_password = self.cleaned_data.get("password")
        if raw_password:
            instance.set_password(raw_password)
        if commit:
            instance.save()
        return instance


class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=PASSWORD_WIDGET, required=False,
                                help_text="Leave blank to keep the current password when editing.")

    class Meta:
        model = Student
        fields = [
            "first_name", "last_name", "email", "contact_number", "password",
            "course", "department", "year_level", "section", "required_hours",
        ]
        widgets = {
            "first_name": TEXT_WIDGET,
            "last_name": TEXT_WIDGET,
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "contact_number": TEXT_WIDGET,
            "course": TEXT_WIDGET,
            "department": TEXT_WIDGET,
            "year_level": forms.NumberInput(attrs={"class": "form-control"}),
            "section": TEXT_WIDGET,
            "required_hours": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        raw_password = self.cleaned_data.get("password")
        if raw_password:
            instance.set_password(raw_password)
        if commit:
            instance.save()
        return instance


class CompanyForm(forms.ModelForm):
    password = forms.CharField(widget=PASSWORD_WIDGET, required=False,
                                help_text="Leave blank to keep the current password when editing.")

    class Meta:
        model = Company
        fields = [
            "company_name", "contact_person", "password", "industry_type",
            "contact_number", "email",
        ]
        widgets = {
            "company_name": TEXT_WIDGET,
            "contact_person": TEXT_WIDGET,
            "industry_type": TEXT_WIDGET,
            "contact_number": TEXT_WIDGET,
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        raw_password = self.cleaned_data.get("password")
        if raw_password:
            instance.set_password(raw_password)
        if commit:
            instance.save()
        return instance


class CoordinatorForm(forms.ModelForm):
    password = forms.CharField(widget=PASSWORD_WIDGET, required=False,
                                help_text="Leave blank to keep the current password when editing.")

    class Meta:
        model = Coordinator
        fields = ["first_name", "last_name", "password", "email", "department"]
        widgets = {
            "first_name": TEXT_WIDGET,
            "last_name": TEXT_WIDGET,
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "department": TEXT_WIDGET,
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        raw_password = self.cleaned_data.get("password")
        if raw_password:
            instance.set_password(raw_password)
        if commit:
            instance.save()
        return instance


class OJTPlacementForm(forms.ModelForm):
    class Meta:
        model = OJTPlacement
        fields = [
            "student", "company", "coordinator", "start_date", "end_date",
            "required_hours", "status",
        ]
        widgets = {
            "student": forms.Select(attrs={"class": "form-select"}),
            "company": forms.Select(attrs={"class": "form-select"}),
            "coordinator": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "required_hours": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = [
            "placement", "log_date", "time_in", "time_out", "rendered_hours",
            "status", "remarks",
        ]
        widgets = {
            "placement": forms.Select(attrs={"class": "form-select"}),
            "log_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "time_in": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "time_out": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "rendered_hours": forms.NumberInput(attrs={"class": "form-control", "step": "0.25"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "remarks": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        """
        Supporting-feature validation for Attendance, integrated with the
        core OJT Placement feature via the `placement` foreign key:
        1. time_out must be later than time_in when both are provided.
        2. A placement cannot have two attendance records on the same
           log_date (duplicate-record prevention).
        """
        cleaned_data = super().clean()
        placement = cleaned_data.get("placement")
        log_date = cleaned_data.get("log_date")
        time_in = cleaned_data.get("time_in")
        time_out = cleaned_data.get("time_out")

        if time_in and time_out and time_out <= time_in:
            self.add_error("time_out", "Time out must be later than time in.")

        if placement and log_date:
            duplicates = Attendance.objects.filter(placement=placement, log_date=log_date)
            if self.instance.pk:
                duplicates = duplicates.exclude(pk=self.instance.pk)
            if duplicates.exists():
                raise forms.ValidationError(
                    f"Duplicate record: an attendance entry for {placement} on "
                    f"{log_date} already exists. Edit the existing record instead "
                    f"of creating a new one."
                )

        return cleaned_data
