from django.db.models.query import QuerySet
from app_auth.models import User,Role
from django.contrib.auth.models import BaseUserManager
# Create your models here.

class FacultyManager(BaseUserManager):

    def get_queryset(self,*args,**kwargs) -> QuerySet:
        result=super().get_queryset(*args,**kwargs)
        return result.filter(role=Role.FACULTY).all()

class Faculty(User):
    base_role=Role.FACULTY
    faculty=FacultyManager()
    class Meta:
        proxy = True
        verbose_name_plural = "Faculty"