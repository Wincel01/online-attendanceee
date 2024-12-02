# from django.db import models
from django.db import models
from django.db.models.query import QuerySet
from app_auth.models import User,Role
from django.contrib.auth.models import BaseUserManager
# Create your models here.

class StudentManager(BaseUserManager):

    def get_queryset(self,*args,**kwargs) -> QuerySet:
        result=super().get_queryset(*args,**kwargs)
        return result.filter(role=Role.STUDENT).all()

class Student(User):
    base_role=Role.STUDENT
    student= StudentManager()
    class Meta:
        proxy = True
        verbose_name_plural = "Students"