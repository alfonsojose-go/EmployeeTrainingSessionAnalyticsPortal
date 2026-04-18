from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("employees/", views.employee_list, name="employee_list"),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:id>/update/', views.employee_update, name='employee_update'),
    path('employees/<int:id>/delete/', views.employee_delete, name='employee_delete'),
    path("courses/", views.course_list, name="course_list"),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:id>/update/', views.course_update, name='course_update'),
    path('courses/<int:id>/delete/', views.course_delete, name='course_delete'),
    path("sessions/", views.session_list, name="session_list"),
    path('sessions/create/', views.session_create, name='session_create'),
    path('sessions/<int:id>/update/', views.session_update, name='session_update'),
    path('sessions/<int:id>/delete/', views.session_delete, name='session_delete'),
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
        views.course_popularity,
        name="course_popularity",
    ),
    path(
    "analytics/employee-transcript/",
    views.employee_transcript,
    name="employee_transcript",
    ),
    # Additional Analytics URLs (FIXED)
    path("analytics/extra/", views.analytics_extra, name="analytics_extra"),
    path("analytics/completion-summary/", views.completion_summary_by_course, name="completion_summary"),
    path("analytics/enrollment-by-session/", views.enrollment_count_by_session, name="enrollment_by_session"),
]
