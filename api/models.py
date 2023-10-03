from django.db import models
from django.contrib.auth.models import  AbstractBaseUser
from api.manager import CustomUserManager 

# Create your models here.

class Role(models.Model):
    ADMIN = 1
    PROMOTER = 2
    
    ROLE_CHOICES = [
        (ADMIN, 'ADMIN'),
        (PROMOTER, 'PROMOTER'),
        ]
    
    role = models.CharField(max_length=20,null=False, choices=ROLE_CHOICES,)

    class Meta:
        db_table = "user_roles"

    def __str__(self):
        return self.role

#User Master
class UserMaster(AbstractBaseUser):
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255,null=True, blank=True,unique=True)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    profile = models.FileField(upload_to='profil_pic/', null=True, blank=True)
        
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = "user_master"
        indexes = [
            models.Index(fields=['email']),
        ]
    
class SharedFiles(models.Model):
    token = models.UUIDField(unique=True)
    shared_by = models.ForeignKey(UserMaster, on_delete=models.CASCADE, related_name = 'shared_files_by')
    shared_to = models.ForeignKey(UserMaster, on_delete=models.CASCADE, related_name = 'shared_files_to', null = True, blank = True)
    file = models.FileField(upload_to='shared_file/')
    created_on = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    class Meta:
        db_table = "user_shareed_files"