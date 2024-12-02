from django.urls import path
from .views import attendance_page,Profile,change_passwd,Dashboard
urlpatterns = [
    path('', attendance_page,name="faculty_index"),
    path('dashboard/', Dashboard,name="faculty_Dashboard"),
    path('profile/', Profile,name="faculty_Profile_page"),
    path('passwd/', change_passwd,name="faculty_change_passwd_page"),
    
]