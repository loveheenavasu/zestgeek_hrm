# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
import uuid


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )
        if extra_fields.get("is_admin") is not True:
            raise ValueError(
                "Superuser must have is_admin=True."
            )
        return self._create_user(email, password, **extra_fields)


class Role(models.Model):
    role_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.role_name


class CustomUser(AbstractBaseUser):
    username = None
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    # is_superuser = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)
    # last_login = None  (Uncomment this if you dont want last_login in the db table)
    USERNAME_FIELD = "email"  # make the user login with the email
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name


class Department(models.Model):
    DEPARTMENT_CHOICES = (
        ('Python', 'Python'),
        ('PHP', 'PHP'),
        ('REACT', 'REACT'),
        ('PHP', 'UI/UX'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    department_name = models.CharField(max_length=100, null=True, blank=True)

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField()
    temperory_address = models.CharField(max_length=100, null=True, blank=True)
    permanent_address = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    alternate_phone_number = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey()

    def __str__(self):
        return self.user.first_name
