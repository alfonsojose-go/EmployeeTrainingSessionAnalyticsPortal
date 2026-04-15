from django.db import models

# Create your models here.
class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ('IT', 'IT'),
        ('HR', 'HR'),
        ('Sales', 'Sales'),
    ]

    full_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return self.full_name


class Course(models.Model):
    CATEGORY_CHOICES = [
        ('Technical', 'Technical'),
        ('Security', 'Security'),
        ('Soft Skills', 'Soft Skills'),
    ]

    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    duration_minutes = models.IntegerField()

    def __str__(self):
        return self.title


class Session(models.Model):
    MODE_CHOICES = [
        ('Online', 'Online'),
        ('In-Person', 'In-Person'),
    ]
    session_date = models.DateField()
    instructor_name = models.CharField(max_length=250)
    mode = models.CharField(max_length=100, choices=MODE_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')

    def __str__(self):
        return f"{self.course.title} - {self.session_date}"


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('ENROLLED', 'ENROLLED'),
        ('COMPLETED', 'COMPLETED'),
        ('CANCELLED', 'CANCELLED'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='enrollments')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ENROLLED')

    class Meta:
        # An employee may not be enrolled more than once in the same session
        unique_together = ['employee', 'session']

    def __str__(self):
        return f"{self.employee.full_name} - {self.session}"

