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
    ROLES_CHOICES = (
        ('SUPERUSER', 'SUPERUSER'),
        ('ADMIN', 'ADMIN'),
        ('PROJECTMANAGER', 'PROJECTMANAGER'),
        ('TEAMLEADER', 'TEAMLEADER'),
        ('EMPLOYEE', 'EMPLOYEE'),
    )
    role_name = models.CharField(max_length=100, choices=ROLES_CHOICES)


    def __str__(self):
        return self.role_name


class CustomUser(AbstractBaseUser):
    username = None
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    personal_email = models.EmailField("email address", unique=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
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
        ('PYTHON', 'PYTHON'),
        ('PHP', 'PHP'),
        ('JS', 'JS'),
        ('UI/UX', 'UI/UX'),
        ('SEO', 'SEO')
    )
    department_name = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class BankDetails(models.Model):
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    iifc_code = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.BigIntegerField(null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class ContactDetails(models.Model):
    address = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Profile(models.Model):
    GENDER_CHOICES = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        ('UNSPECIFIED', 'UNSPECIFIED'),
    )
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.CharField(max_length=100, null=True, blank=True)
    contact = models.ManyToManyField(ContactDetails)
    # temperory_address = models.CharField(max_length=100, null=True, blank=True)
    # permanent_address = models.CharField(max_length=100, null=True, blank=True)
    # phone_number = models.CharField(max_length=100, null=True, blank=True)
    # alternate_phone_number = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    bank = models.ForeignKey(BankDetails, on_delete=models.CASCADE)
    joined_date = models.DateField()
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.user.first_name



