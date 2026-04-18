from django import forms
from django.core.exceptions import ValidationError

from .models import Enrollment, Employee, Course, Session


class EnrollmentForm(forms.ModelForm):
    """Form used to create or update enrollment records."""

    class Meta:
        model = Enrollment
        fields = ["employee", "session", "status"]
        widgets = {
            "employee": forms.Select(attrs={"class": "form-select"}),
            "session": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        """Block duplicate enrollment for the same employee and session."""
        cleaned = super().clean()
        employee = cleaned.get("employee")
        session = cleaned.get("session")
        if employee and session:
            qs = Enrollment.objects.filter(employee=employee, session=session)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(
                    "This employee is already enrolled in this session."
                )
        return cleaned


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = '__all__'