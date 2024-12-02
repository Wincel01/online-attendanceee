from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from records.models import Attendance,Subjects,Period
from student.models import Student
from .models import Faculty
from app_auth.models import Role
from django.contrib import messages
from datetime import date
# Create your views here.

@login_required
def attendance_page(request):
    if request.method == "POST":
        Date=request.POST.get('Date')
        period=request.POST.get('period')
        subject=request.POST.get('subject')
        if period and subject:
            subject=Subjects.objects.filter(name=subject).get()
            students=request.POST.getlist('student-id')
            # print("student id: ",students)
            if request.user.role == Role.FACULTY:
                for i in students:
                    print("student: ",i)
                    if Date:
                        Date=Date
                        # student =Student.objects.filter(Department_no=i).get()
                        # attendance,created=Attendance.objects.get_or_create(subject=subject,date=Date,period=period,faculty_id=request.user,student_id=student,department_name=request.user.department_name)
                        # if created:
                        #     print("new record")
                            # messages.add_message(request,messages.SUCCESS,"New record created")
                        # attendance.present=request.POST[i]
                        # print(vars(attendance))
                        # attendance.save()
                    else:
                        Date=date.today()
                        # student =Student.objects.filter(Department_no=i).get()
                        # attendance,created=Attendance.objects.get_or_create(subject=subject,date=date.today(),period=period,faculty_id=request.user,student_id=student,department_name=request.user.department_name)
                        # if created:
                        #     print("new record")
                    student =Student.objects.filter(Department_no=i).get()
                    attendance,created=Attendance.objects.get_or_create(subject=subject,date=Date,period=period,faculty_id=request.user,student_id=student,department_name=request.user.department_name)
                    attendance.present=request.POST[i]
                    print(vars(attendance))
                    attendance.save()

                messages.add_message(request,messages.SUCCESS,"record saved successfully")
                data={
                "attendance":Attendance.objects.filter(date=Date,department_name=request.user.department_name).all(),
                }
                return render(request,'faculty/attendance.html',context=data)
            else:
                return HttpResponse("not a faculty")
        else:
            messages.add_message(request,messages.WARNING,"please select a subject and period")
            return redirect('faculty_index')
    else:
        # print("vars ",vars(Period))
        print("date :",date.today())
        data={
            "subjects":Subjects.objects.filter(department_name=request.user.department_name).all(),
            "periods":Period._member_names_,
            "Students": Student.student.filter(department_name=request.user.department_name).all()
        }
        return render(request,'faculty/attendance.html',context=data)



@login_required
def Dashboard(request):
    if request.user.role == Role.FACULTY:
        p_labels=[]
        p_data=[]
        a_data=[]
        for student in Student.student.filter(department_name=request.user.department_name).all():
            # total=Attendance.objects.filter(department_name=request.user.department_name,student_id=student).all().values_list('date').distinct().count()

            total=Attendance.objects.filter(student_id=student,department_name=request.user.department_name).all().values_list('date').distinct().count()
            present=Attendance.objects.filter(student_id=student,present=True,department_name=request.user.department_name).all().values_list('date').distinct().count()
            absent=total-present
            # percentage=(present/total)*100
            p_labels.append(student.Department_no)
            p_data.append(present)
            a_data.append(absent)
       
        data={
            "total_attendance":Attendance.objects.filter(department_name=request.user.department_name).all().values_list('date').distinct().count(),
            "staff_attendance":Attendance.objects.filter(faculty_id=request.user,subject=1,department_name=request.user.department_name).all().values_list('date').distinct().count(),
            "p_labels":p_labels,
            "p_data":p_data,
            "a_data":a_data
        }
    else:
        data={
            "total_attendance":Attendance.objects.filter(department_name=request.user.department_name).all().values_list('date').distinct().count(),
        }
    return render(request,'dashboard.html',context=data)


@login_required
def Profile(request):

    if request.user.role == Role.FACULTY:
        if request.method== 'POST':
            email=request.POST['email']
            fname=request.POST['fname']
            lname=request.POST['lname']
            fac=Faculty.objects.filter(username=request.user.username,department_name=request.user.department_name).get()
            fac.email=email
            fac.first_name=fname
            fac.last_name=lname
            fac.save()
            return redirect('faculty_index')
        else:
            data={
                "faculty":Faculty.objects.filter(username=request.user.username).get()
            }
            return render(request,'faculty/profile.html',context=data)
    else:
        messages.add_message(request,messages.ERROR,"Un-authorized login.Not a staff")
        return redirect('auth_redirect')


@login_required
def change_passwd(request):
    if request.user.role == Role.FACULTY:
        if request.method== 'POST':
            password=request.POST['password']
            c_password=request.POST['c_password']
            fac=Faculty.objects.filter(username=request.user.username,department_name=request.user.department_name).get()
            if password == c_password:
                fac.set_password(password)
                fac.save()
                return redirect('faculty_index')
            else:
                messages.add_message(request,messages.WARNING,"password and conform password mismatched")
                return redirect('faculty_index')
        else:
            return render(request,'faculty/changepasswd.html')
    else:
        messages.add_message(request,messages.ERROR,"Un-authorized login.Not a staff")
        return redirect('auth_redirect')




