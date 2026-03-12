from django.urls import path
from . import views
app_name = 'student'
urlpatterns = [
    path('', views.student_login, name='login'),
    path('display/', views.student_dashboard, name='student_dashboard'),
    path('add/', views.add_student, name='add_student'),
    path('view/', views.view_students, name='view_students'),
    path('edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('logout/', views.student_logout, name='logout'),
    path('high-risk/', views.high_risk_students, name='high_risk_students'),
    path('medium-risk/', views.medium_risk_students, name='medium_risk_students'),
    path('low-risk/', views.low_risk_students, name='low_risk_students'),
    path('alert-dashboard/', views.alert_dashboard, name='alert_dashboard'),
    path('counselling/<int:student_id>/', views.counselling_page, name='counselling'),
    path('counselling-history/<int:student_id>/',  views.counselling_history, name='counseling_dashboard'),
]

