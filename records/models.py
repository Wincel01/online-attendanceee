from django.db import models
from student.models import Student
from faculty.models import Faculty
from app_auth.models import Department
# Create your models here.

class Period(models.TextChoices):
    FIRST="1"
    SECOND="2"
    THIRD="3"
    FOURTH="4"
    FIFTH="5"
    SIXTH="6"
    SEVENTH="7"

class Subjects(models.Model):
    department_name=models.ForeignKey(to=Department,on_delete=models.CASCADE,related_name='Department_subject')
    name=models.CharField(max_length=100,blank=True,null=True)
    class Meta:
        verbose_name_plural = "Subjects"

    def __str__(self) -> str:
        return str(self.name)


class Attendance(models.Model):
    department_name=models.ForeignKey(to=Department,on_delete=models.CASCADE,related_name='Department_attendance')
    student_id=models.ForeignKey(to=Student,on_delete=models.CASCADE,related_name="Student_id")
    faculty_id=models.ForeignKey(to=Faculty,on_delete=models.CASCADE,related_name="Faculty_id")
    date=models.DateField(blank=True,null=True)
    present=models.BooleanField(default=False,null=True,blank=True)
    period=models.CharField(max_length=50,choices=Period.choices,blank=True)
    subject=models.ForeignKey(to=Subjects,on_delete=models.DO_NOTHING,related_name="Subject")
    class Meta:
        verbose_name_plural = "Attendance"