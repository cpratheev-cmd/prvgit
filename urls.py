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
]

