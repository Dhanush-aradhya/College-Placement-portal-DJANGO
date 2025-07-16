# home/urls.py
from django.urls import path
from home import views

urlpatterns = [
    # ... your other url patterns ...
    path("", views.index, name="home"),
    path("userlogin/", views.userlogin_view, name='userlogin'),
    path("adminlogin/", views.adminlogin_view, name='adminlogin'),
    path('userportal/', views.userportal, name='userportal'),
    path('adminportal/', views.adminportal, name='adminportal'),
    path('update-password/', views.update_password, name='update_password'),
    path('upload-details/', views.upload_details, name='upload_details'),
    path('logout/', views.logout_view, name='logout'),
    path('adminportal/search-student/', views.faculty_search_student_view, name='faculty_search_student'),
    path('adminportal/change-password/', views.faculty_password_change_view, name='faculty_password_change'),
    path('adminportal/download_excel/', views.download_students_excel_view, name='download_students_excel'),
]