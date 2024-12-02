from django.shortcuts import render,HttpResponse,redirect
import csv
from django.contrib.auth.decorators import login_required
from app_auth.models import Department
from student.models import Student
from faculty.models import Faculty
from .models import Attendance,Subjects

@login_required
def report_view(request):
    data={
        "faculty":Faculty.faculty.filter(department_name=request.user.department_name).all(),
        "students":Student.student.filter(department_name=request.user.department_name).all(),
    }
    return render(request,'report.html',context=data)





@login_required
def report(request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="AttendanceReport.csv"'
        department=Department.objects.filter(id=request.user.department_name.id).get()
        print(vars(department))
        if request.method == 'POST':
            # return HttpResponse('post method')
            faculty_id=request.POST.get('fac_id')
            to_day=request.POST.get('date')
            student_id=request.POST.get('Stud_id')
            if faculty_id and student_id and to_day:
                stud=Student.objects.filter(Department_no=student_id).get()
                fac=Faculty.objects.filter(Department_no=faculty_id).get()
                attendance=Attendance.objects.filter(faculty_id=fac,student_id=stud,date=to_day).all()
            elif faculty_id and student_id:
                stud=Student.objects.filter(Department_no=student_id).get()
                fac=Faculty.objects.filter(Department_no=faculty_id).get()
                attendance=Attendance.objects.filter(faculty_id=fac,student_id=stud).all()
            elif faculty_id and to_day:
                fac=Faculty.objects.filter(Department_no=faculty_id).get()
                attendance=Attendance.objects.filter(faculty_id=fac,date=to_day).all()
            elif faculty_id:
                
                fac=Faculty.objects.filter(Department_no=faculty_id).get()
                attendance=Attendance.objects.filter(faculty_id=fac).all()
            elif student_id:
                 stud=Student.objects.filter(Department_no=student_id).get()
                 attendance=Attendance.objects.filter(student_id=stud).all()
            elif to_day:
                 attendance=Attendance.objects.filter(date=to_day).all()
            else:
                attendance=Attendance.objects.filter(department_name=request.user.department_name).all()
        else:
            attendance=Attendance.objects.filter(department_name=request.user.department_name).all()
        writer = csv.writer(response)
        writer.writerow(['Sno','Date','Present','Period','Subject','Faculty_id','Faculty_name','Student_id','Student_name','Department'])
        
            # return response
        for count, attend in enumerate(attendance):
                
            subject=Subjects.objects.filter(name=attend.subject).get()
            fac=Faculty.faculty.filter(username=attend.faculty_id).get()
            stud=Student.student.filter(username=attend.student_id).get()
            writer.writerow([count+1,str(attend.date),attend.present,attend.period,subject.name,fac.Department_no,fac.get_full_name(),stud.Department_no,stud.get_full_name(),department.name])
        return response


