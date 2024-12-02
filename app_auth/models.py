from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy
from django.conf import settings
from cryptography.fernet import Fernet
# Create your models here.

f=Fernet(settings.ENCRYPTION_KEY)

class Role(models.TextChoices):
    ADMIN="ADMIN","Admin"
    STUDENT="STUDENT","Student"
    FACULTY="FACULTY","Faculty"

class UserManager(BaseUserManager):

    def create_superuser(self,username,email,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_active',True)
        other_fields.setdefault('is_superuser',True)

        return self.create_user(username,email,password,**other_fields)
    def create_user(self,username,email,password,**other_fileds):
        email=self.normalize_email(email)
        user=self.model(username=username,email=email,**other_fileds)
        if len(password) < 30:
            user.passwd=f.encrypt(self.password.encode()).decode()
            user.set_password(password)
        return user

class Department(models.Model):
    name=models.CharField(max_length=100,blank=True)

    def __str__(self) -> str:
        return str(self.name)

class User(AbstractUser):
    department_name=models.ForeignKey(to=Department,on_delete=models.CASCADE,related_name="Department",null=True)
    Department_no=models.CharField(gettext_lazy("Department_no"),max_length=100,blank=True,unique=True)
    Date_Of_Birth=models.DateField(blank=True,null=True)
    Mob_no=models.PositiveIntegerField(blank=True,null=True)
    role=models.CharField(max_length=10,choices=Role.choices,blank=True)
    passwd=models.TextField(blank=True,null=True)
    base_role=Role.ADMIN
    
    def get_pass(self) -> str:
        if self.passwd:
            decrypt_token=f.decrypt(self.passwd.encode()).decode()
            print(decrypt_token)
        return decrypt_token

    def save(self,*args,**kwargs):

        if not self.pk:
            self.role=self.base_role
            self.username=str(self.username).upper()
            self.Department_no=str(self.Department_no).upper()
            self.first_name=str(self.first_name).upper()
            self.last_name=str(self.last_name).upper()
            if len(self.password) < 30:
                self.passwd=f.encrypt(self.password.encode()).decode()
                self.set_password(self.password)
            return super().save(*args,**kwargs)
        else:
            self.first_name=str(self.first_name).upper()
            self.last_name=str(self.last_name).upper()
            self.username=str(self.username).upper()
            self.Department_no=str(self.Department_no).upper()
            if len(self.password) < 30:
                self.passwd=f.encrypt(self.password.encode()).decode()
                self.set_password(self.password)
            return super().save(*args,**kwargs)