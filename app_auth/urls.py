from django.urls import path
from .views import login_page,auth_redirect,logout_page
urlpatterns = [
    path('login/', login_page,name="login_page"),
    path('', auth_redirect,name="auth_redirect"),
    path('logout/', logout_page,name="logout_page"),
]