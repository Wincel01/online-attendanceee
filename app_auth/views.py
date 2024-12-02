from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from .models import Role
from django.contrib.auth.decorators import login_required

# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username=str(request.POST.get('username')).upper()
        password=request.POST.get('password')
        print(f"username :{username} password :{password}")
        
        user=authenticate(username=username,password=password)
        if user:
            print("authendicated user")
            login(request,user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.add_message(request, messages.ERROR, "Credentials mismatched, Please enter the correct username and password")
            print("un-authendicated user")

        
        

        
    # messages.add_message(request, messages.INFO, "Hello world.")
    return render(request,'auth/login.html')




@login_required
def auth_redirect(request):
    if request.user.role == Role.FACULTY:
        return redirect('faculty_index')
    if request.user.role == Role.STUDENT:
        return redirect('student_index')
    else:
        return redirect('auth_redirect')
    

def logout_page(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)