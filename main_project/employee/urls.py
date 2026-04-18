from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("employees/", views.employee_list, name="employee_list"),
    path("courses/", views.course_list, name="course_list"),
    path("sessions/", views.session_list, name="session_list"),
    path("enrollments/", views.enrollment_list, name="enrollment_list"),
    path("enrollments/add/", views.enrollment_create, name="enrollment_create"),
    path("enrollments/<int:pk>/edit/", views.enrollment_update, name="enrollment_update"),
    path("analytics/", views.analytics_hub, name="analytics_hub"),
    path(
        "analytics/department-participation/",
        views.department_participation,
        name="department_participation",
    ),
    path(
        "analytics/course-popularity/",
        views.course_popularity_placeholder,
        name="course_popularity",
    ),
    path(
    "analytics/employee-transcript/",
    views.employee_transcript,
    name="employee_transcript",
    ),
    path(
        "analytics/extra/",
        views.analytics_extra_placeholder,
        name="analytics_extra",
    ),
]
