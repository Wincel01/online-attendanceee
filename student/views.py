from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from app_auth.models import Role
from records.models import Attendance,Subjects
from django.contrib import messages
from .models import Student
from faculty.models import Faculty
import csv
# Create your views here.

@login_required
def dashboard(request):
    if request.user.role == Role.STUDENT:
        print("role",request.user.role)
        total=Attendance.objects.filter(student_id=request.user,department_name=request.user.department_name).all().count()
        present=Attendance.objects.filter(student_id=request.user,present=True,department_name=request.user.department_name).all().count()
        percentage=(present/total)*100
        print(percentage)
        total_days=Attendance.objects.filter(student_id=request.user,department_name=request.user.department_name).all().values_list('date').distinct().count()
        p_days=Attendance.objects.filter(student_id=request.user,present=True,department_name=request.user.department_name).all().values_list('date').distinct().count()
        a_days=total_days-p_days
        labels=["present","absent"]
        data=[p_days,a_days]
        data={
            "total_attendance":total_days,
            "absent":a_days,
            "present":p_days,
            "labels":labels,
            "data":data

        }
        return render(request,'dashboard.html',context=data)
    else:
        messages.add_message(request,messages.ERROR,"Un-authorized login.Not a Student")
        return redirect('auth_redirect')
    



@login_required
def change_passwd(request):
    if request.user.role == Role.STUDENT:
        
        if request.method== 'POST':
            password=request.POST['password']
            c_password=request.POST['c_password']
            stud=Student.objects.filter(username=request.user.username).get()
            if password == c_password:
                stud.set_password(password)
                stud.save()
                return redirect('student_index')
            else:
                messages.add_message(request,messages.WARNING,"password and conform password mismatched")
                return redirect('student_index')
        else:
            return render(request,'student/changepasswd.html')
    else:
        messages.add_message(request,messages.ERROR,"Un-authorized login.Not a staff")
        return redirect('auth_redirect')



@login_required
def Profile(request):
    if request.user.role == Role.STUDENT:
        if request.method== 'POST':
            email=request.POST['email']
            fname=request.POST['fname']
            lname=request.POST['lname']
            fac=Student.objects.filter(username=request.user.username,department_name=request.user.department_name).get()
            fac.email=email
            fac.first_name=fname
            fac.last_name=lname
            fac.save()
            return redirect('student_index')
        else:
            data={
                "student":Student.objects.filter(username=request.user.username).get()
            }
            return render(request,'student/profile.html',context=data)
    else:
        messages.add_message(request,messages.ERROR,"Un-authorized login.Not a staff")
        return redirect('auth_redirect')



