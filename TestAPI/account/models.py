from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from TestAPI.validators import CustomPasswordValidator
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Role(models.TextChoices):
    USER       = 'user'
    ADMIN      = 'admin'
    SUPERADMIN = 'super admin'

class UserProfile(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField()
    address = models.CharField(max_length=200)
    city    = models.CharField(max_length=50)
    role    = models.CharField(max_length=50, choices=Role.choices, default=Role.USER)
    photo   = models.ImageField(upload_to = 'profile_photos/%Y/%m/%d', blank = True, null = True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    
    def __str__(self):
        return f'{self.email} - {self.role}'

    def set_password(self, raw_password):
        validator = CustomPasswordValidator()
        validator.validate(raw_password)
        super().set_password(raw_password)
        
