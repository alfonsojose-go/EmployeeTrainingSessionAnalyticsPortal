from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EnrollmentForm
from .models import Course, Employee, Enrollment, Session


def home(request):
    """Render the portal landing page."""
    return render(request, "employee/home.html")


def employee_list(request):
    """List employees with an optional department filter."""
    employees = Employee.objects.all().order_by("full_name")
    department = request.GET.get("department") or ""
    if department:
        employees = employees.filter(department=department)
    context = {
        "employees": employees,
        "department": department,
        "department_choices": Employee.DEPARTMENT_CHOICES,
    }
    return render(request, "employee/employee_list.html", context)


def course_list(request):
    """List courses with an optional category filter."""
    courses = Course.objects.all().order_by("title")
    category = request.GET.get("category") or ""
    if category:
        courses = courses.filter(category=category)
    context = {
        "courses": courses,
        "category": category,
        "category_choices": Course.CATEGORY_CHOICES,
    }
    return render(request, "employee/course_list.html", context)


def session_list(request):
    """List sessions with optional date-range and instructor filters."""
    sessions = Session.objects.select_related("course").all().order_by(
        "-session_date", "course__title"
    )
    date_from = request.GET.get("date_from") or ""
    date_to = request.GET.get("date_to") or ""
    instructor = request.GET.get("instructor") or ""
    if date_from:
        sessions = sessions.filter(session_date__gte=date_from)
    if date_to:
        sessions = sessions.filter(session_date__lte=date_to)
    if instructor:
        sessions = sessions.filter(instructor_name__icontains=instructor.strip())
    context = {
        "sessions": sessions,
        "date_from": date_from,
        "date_to": date_to,
        "instructor": instructor,
    }
    return render(request, "employee/session_list.html", context)


def enrollment_list(request):
    """List enrollments with status and employee-department filters."""
    # Eager-load related objects used in the table to reduce per-row queries.
    enrollments = (
        Enrollment.objects.select_related("employee", "session__course")
        .all()
        .order_by("-session__session_date", "employee__full_name")
    )
    status = request.GET.get("status") or ""
    department = request.GET.get("department") or ""
    if status:
        enrollments = enrollments.filter(status=status)
    if department:
        enrollments = enrollments.filter(employee__department=department)
    context = {
        "enrollments": enrollments,
        "status": status,
        "department": department,
        "status_choices": Enrollment.STATUS_CHOICES,
        "department_choices": Employee.DEPARTMENT_CHOICES,
    }
    return render(request, "employee/enrollment_list.html", context)


def enrollment_create(request):
    """Create a new enrollment and redirect to the enrollment list."""
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("enrollment_list")
    else:
        form = EnrollmentForm(initial={"status": "ENROLLED"})
    return render(
        request,
        "employee/enrollment_form.html",
        {"form": form, "title": "Add enrollment"},
    )


def enrollment_update(request, pk):
    """Update an existing enrollment record."""
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == "POST":
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect("enrollment_list")
    else:
        form = EnrollmentForm(instance=enrollment)
    return render(
        request,
        "employee/enrollment_form.html",
        {"form": form, "title": "Update enrollment"},
    )


def analytics_hub(request):
    """Render the analytics dashboard links page."""
    return render(request, "employee/analytics_hub.html")


def department_participation(request):
    """
    Completed trainings per employee department.
    Optional filter: course category (only completed enrollments for sessions in that category).
    """
    category = request.GET.get("category") or ""
    qs = Enrollment.objects.filter(status="COMPLETED").select_related(
        "employee", "session__course"
    )
    if category:
        qs = qs.filter(session__course__category=category)

    rows = (
        qs.values("employee__department")
        .annotate(completed_trainings=Count("id"))
        .order_by("-completed_trainings", "employee__department")
    )
    context = {
        "rows": rows,
        "category": category,
        "category_choices": Course.CATEGORY_CHOICES,
    }
    return render(request, "employee/analytics_department.html", context)


def analytics_placeholder(request, page_title: str):
    """Render a placeholder page for analytics reports not implemented yet."""
    return render(
        request,
        "employee/analytics_placeholder.html",
        {"page_title": page_title},
    )


def course_popularity_placeholder(request):
    """Placeholder endpoint for the course popularity report."""
    return analytics_placeholder(request, "Course Popularity")


def employee_transcript_placeholder(request):
    """Placeholder endpoint for the employee transcript report."""
    return analytics_placeholder(request, "Employee Training Transcript")


def analytics_extra_placeholder(request):
    """Placeholder endpoint for additional analytics reports."""
    return analytics_placeholder(request, "Additional analytics")
