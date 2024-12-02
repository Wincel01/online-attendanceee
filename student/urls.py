from django.urls import path
from .views import dashboard,change_passwd,Profile
urlpatterns = [
    path('', dashboard,name="student_index"),
    path('change_pass/', change_passwd,name="student_change_pass_page"),
    path('profile/', Profile,name="student_profile_page"),
]