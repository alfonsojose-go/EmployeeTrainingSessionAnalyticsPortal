from django.contrib import admin
from .models import Employee, Course, Session, Enrollment


# Register your models here.
admin.site.register(Employee)
admin.site.register(Course)
admin.site.register(Session)
admin.site.register(Enrollment)
