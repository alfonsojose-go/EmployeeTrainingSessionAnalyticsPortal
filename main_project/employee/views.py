from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EnrollmentForm, EmployeeForm, CourseForm, SessionForm
from .models import Course, Employee, Enrollment, Session



def home(request):
    """Render the portal landing page."""
    context = {
        "total_employees": Employee.objects.count(),
        "total_courses": Course.objects.count(),
        "total_sessions": Session.objects.count(),
        "total_enrollments": Enrollment.objects.count(),
    }
    return render(request, "employee/home.html", context)


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

def employee_create(request):
    """Create a new employee and redirect to the employee list."""
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("employee_list")

    else:  # GET request (or other methods)
        form = EmployeeForm()

    return render(
        request,
        "employee/employee_form.html",
        {"form": form, "title": "Add Employee"},
    )

def employee_update(request, id):
    employee = Employee.objects.get(id=id)
    form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')

    return render(request,
                  'employee/employee_form.html',
                  {'form': form, 'title': 'Edit Employee'}  # ← Merge into one dict
                  )


def employee_delete(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()

    return  redirect('employee_list')

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

def course_create(request):
    """Create a new course and redirect to the course list."""
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("course_list")

    else:  # GET request (or other methods)
        form = CourseForm()

    return render(
        request,
        "employee/course_form.html",
        {"form": form, "title": "Add Course"},
    )

def course_update(request, id):
    course = Course.objects.get(id=id)
    form = CourseForm(instance=course)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')

    return render(request,
                  'employee/course_form.html',
                  {'form': form, 'title': 'Edit Course'}  # ← Merge into one dict
                  )


def course_delete(request, id):
    course = Course.objects.get(id=id)
    course.delete()

    return  redirect('course_list')


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

def session_create(request):
    """Create a new session and redirect to the session list."""
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("session_list")

    else:  # GET request (or other methods)
        form = SessionForm()

    return render(
        request,
        "employee/session_form.html",
        {"form": form, "title": "Add Session"},
    )

def session_update(request, id):
    session = Session.objects.get(id=id)
    form = SessionForm(instance=session)

    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('session_list')

    return render(request,
                  'employee/session_form.html',
                  {'form': form, 'title': 'Edit Session'}  # ← Merge into one dict
                  )


def session_delete(request, id):
    session = Session.objects.get(id=id)
    session.delete()

    return  redirect('session_list')


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
    context = {
        "total_employees": Employee.objects.count(),
        "total_courses": Course.objects.count(),
        "total_sessions": Session.objects.count(),
        "total_enrollments": Enrollment.objects.count(),
    }
    return render(request, "employee/analytics_hub.html", context)


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


def course_popularity(request):
    """
    Identify which courses have the most enrollments.
    Count enrollments grouped by course and display success rate.
    """
    courses = Course.objects.all()
    course_data = []

    for course in courses:
        # Get all sessions for this course
        sessions = Session.objects.filter(course=course)

        # Count total enrollments for this course
        total_enrollments = Enrollment.objects.filter(session__in=sessions).count()

        # Count completed enrollments for this course
        completed_enrollments = Enrollment.objects.filter(
            session__in=sessions,
            status='COMPLETED'
        ).count()

        # Calculate success rate
        if total_enrollments > 0:
            success_rate = (completed_enrollments / total_enrollments) * 100
        else:
            success_rate = 0

        course_data.append({
            'course_title': course.title,
            'total_enrollments': total_enrollments,
            'success_rate': success_rate,
        })

    # Sort by total_enrollments (highest first)
    course_data.sort(key=lambda x: x['total_enrollments'], reverse=True)

    context = {
        'course_data': course_data,
    }

    return render(request, "employee/analytics_course_popularity.html", context)



def employee_transcript(request):
    """
    Show the training transcript for one selected employee.
    Displays course title, session date, and enrollment status.
    """
    employees = Employee.objects.all().order_by("full_name")
    selected_employee_id = request.GET.get("employee") or ""

    selected_employee = None
    transcript_rows = Enrollment.objects.none()

    if selected_employee_id:
        selected_employee = get_object_or_404(Employee, pk=selected_employee_id)
        transcript_rows = (
            Enrollment.objects.select_related("session__course", "employee")
            .filter(employee=selected_employee)
            .order_by("-session__session_date", "session__course__title")
        )

    context = {
        "employees": employees,
        "selected_employee_id": selected_employee_id,
        "selected_employee": selected_employee,
        "transcript_rows": transcript_rows,
    }
    return render(request, "employee/analytics_employee_transcript.html", context)


def analytics_extra_placeholder(request):
    """Placeholder endpoint for additional analytics reports."""
    return analytics_placeholder(request, "Additional analytics")

def analytics_extra(request):
    """
    Additional analytics hub page showing links to:
    1. Completion summary by course
    2. Enrollment count by session
    """
    from .models import Course, Session, Enrollment

    total_courses = Course.objects.count()
    total_sessions = Session.objects.count()
    total_enrollments = Enrollment.objects.count()

    context = {
        'total_courses': total_courses,
        'total_sessions': total_sessions,
        'total_enrollments': total_enrollments,
    }

    return render(request, "employee/analytics_placeholder.html", context)

def completion_summary_by_course(request):
    """
    Show completion summary for each course.
    Displays: Course Title, Total Enrollments, Completed, Cancelled, Enrolled (in progress), Completion Rate
    """
    courses = Course.objects.all()
    course_data = []

    for course in courses:
        # Get all sessions for this course
        sessions = Session.objects.filter(course=course)

        # Get enrollment counts by status
        total_enrollments = Enrollment.objects.filter(session__in=sessions).count()
        completed = Enrollment.objects.filter(session__in=sessions, status='COMPLETED').count()
        cancelled = Enrollment.objects.filter(session__in=sessions, status='CANCELLED').count()
        enrolled = Enrollment.objects.filter(session__in=sessions, status='ENROLLED').count()

        # Calculate completion rate
        if total_enrollments > 0:
            completion_rate = (completed / total_enrollments) * 100
        else:
            completion_rate = 0

        course_data.append({
            'course_title': course.title,
            'category': course.get_category_display(),
            'total_enrollments': total_enrollments,
            'completed': completed,
            'cancelled': cancelled,
            'enrolled': enrolled,
            'completion_rate': completion_rate,
        })

    # Sort by completion rate (highest first)
    course_data.sort(key=lambda x: x['completion_rate'], reverse=True)

    context = {
        'course_data': course_data,
    }

    return render(request, "employee/analytics_completion_summary.html", context)

def enrollment_count_by_session(request):
    """
    Show enrollment count for each session.
    Displays: Course Title, Session Date, Instructor, Mode, Total Enrollments, Status Breakdown
    """
    sessions = Session.objects.all().order_by('-session_date')
    session_data = []

    for session in sessions:
        # Get enrollment counts for this session
        total_enrollments = Enrollment.objects.filter(session=session).count()
        completed = Enrollment.objects.filter(session=session, status='COMPLETED').count()
        cancelled = Enrollment.objects.filter(session=session, status='CANCELLED').count()
        enrolled = Enrollment.objects.filter(session=session, status='ENROLLED').count()

        # Calculate fill rate (if there's a max capacity field)
        # Add if you have a capacity field in Session model
        fill_rate = 0
        if hasattr(session, 'capacity') and session.capacity and session.capacity > 0:
            fill_rate = (total_enrollments / session.capacity) * 100

        session_data.append({
            'course_title': session.course.title,
            'session_date': session.session_date,
            'instructor': session.instructor_name,
            'mode': session.get_mode_display(),
            'total_enrollments': total_enrollments,
            'completed': completed,
            'cancelled': cancelled,
            'enrolled': enrolled,
            'fill_rate': fill_rate,
        })

    # Sort by total enrollments (most popular sessions first)
    session_data.sort(key=lambda x: x['total_enrollments'], reverse=True)

    context = {
        'session_data': session_data,
    }

    return render(request, "employee/analytics_enrollment_by_session.html", context)