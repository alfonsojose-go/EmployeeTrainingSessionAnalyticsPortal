from datetime import date, timedelta

from employee.models import Course, Employee, Enrollment, Session


def seed_employees():
    employee_seed = [
        ("John Smith", "john.smith@company.com", "IT"),
        ("Alice Chen", "alice.chen@company.com", "IT"),
        ("Bob Lee", "bob.lee@company.com", "HR"),
        ("Diana Cruz", "diana.cruz@company.com", "HR"),
        ("Ethan Park", "ethan.park@company.com", "Sales"),
        ("Fiona Hall", "fiona.hall@company.com", "Sales"),
        ("Grace Lin", "grace.lin@company.com", "IT"),
        ("Henry Wu", "henry.wu@company.com", "HR"),
        ("Ivy Tran", "ivy.tran@company.com", "Sales"),
        ("Kevin Zhao", "kevin.zhao@company.com", "IT"),
    ]
    employees = {}
    for full_name, email, department in employee_seed:
        employee, _ = Employee.objects.get_or_create(
            email=email,
            defaults={"full_name": full_name, "department": department},
        )
        employees[email] = employee
    return employees


def seed_courses():
    course_seed = [
        ("Python Basics", "Technical", 120),
        ("Django Essentials", "Technical", 150),
        ("Security Awareness", "Security", 90),
        ("Phishing Defense", "Security", 60),
        ("Business Communication", "Soft Skills", 100),
    ]
    courses = {}
    for title, category, duration_minutes in course_seed:
        course, _ = Course.objects.get_or_create(
            title=title,
            defaults={
                "category": category,
                "duration_minutes": duration_minutes,
            },
        )
        courses[title] = course
    return courses


def seed_sessions(courses):
    today = date.today()
    session_seed = [
        ("Python Basics", -20, "Dr. Lee", "Online"),
        ("Python Basics", -10, "Dr. Lee", "In-Person"),
        ("Django Essentials", -7, "Ms. Carter", "Online"),
        ("Security Awareness", -15, "A. Watts", "In-Person"),
        ("Security Awareness", -3, "A. Watts", "Online"),
        ("Phishing Defense", -1, "N. Patel", "Online"),
        ("Business Communication", -12, "R. Gomez", "In-Person"),
        ("Business Communication", 5, "R. Gomez", "Online"),
    ]
    sessions = []
    for course_title, day_offset, instructor_name, mode in session_seed:
        session, _ = Session.objects.get_or_create(
            course=courses[course_title],
            session_date=today + timedelta(days=day_offset),
            instructor_name=instructor_name,
            mode=mode,
        )
        sessions.append(session)
    return sessions


def seed_enrollments(employees, sessions):
    enrollment_seed = [
        ("john.smith@company.com", 0, "COMPLETED"),
        ("alice.chen@company.com", 0, "COMPLETED"),
        ("bob.lee@company.com", 0, "ENROLLED"),
        ("diana.cruz@company.com", 1, "COMPLETED"),
        ("ethan.park@company.com", 1, "CANCELLED"),
        ("fiona.hall@company.com", 2, "COMPLETED"),
        ("grace.lin@company.com", 2, "ENROLLED"),
        ("henry.wu@company.com", 3, "COMPLETED"),
        ("ivy.tran@company.com", 3, "ENROLLED"),
        ("kevin.zhao@company.com", 4, "COMPLETED"),
        ("john.smith@company.com", 4, "COMPLETED"),
        ("alice.chen@company.com", 5, "ENROLLED"),
        ("bob.lee@company.com", 5, "COMPLETED"),
        ("diana.cruz@company.com", 6, "COMPLETED"),
        ("ethan.park@company.com", 6, "ENROLLED"),
        ("fiona.hall@company.com", 7, "ENROLLED"),
        ("grace.lin@company.com", 7, "COMPLETED"),
        ("henry.wu@company.com", 1, "COMPLETED"),
        ("ivy.tran@company.com", 2, "CANCELLED"),
        ("kevin.zhao@company.com", 3, "COMPLETED"),
    ]

    for email, session_index, status in enrollment_seed:
        Enrollment.objects.update_or_create(
            employee=employees[email],
            session=sessions[session_index],
            defaults={"status": status},
        )


employees = seed_employees()
courses = seed_courses()
sessions = seed_sessions(courses)
seed_enrollments(employees, sessions)

print("Seed complete.")
print("Employees:", Employee.objects.count())
print("Courses:", Course.objects.count())
print("Sessions:", Session.objects.count())
print("Enrollments:", Enrollment.objects.count())
