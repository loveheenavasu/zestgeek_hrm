# users/models.py
from django.db import models
from user_management.base import BaseModel
from inventory.models import Inventory
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Role(BaseModel):
    role_name = models.CharField(max_length=100)

    def __str__(self):
        return self.role_name


class Department(BaseModel):
    # DEPARTMENT_CHOICES = (
    #     ('PYTHON', 'PYTHON'),
    #     ('PHP', 'PHP'),
    #     ('JS', 'JS'),
    #     ('UI/UX', 'UI/UX'),
    #     ('SEO', 'SEO')
    # )
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name


class CustomUser(AbstractBaseUser, BaseModel):
    GENDER_CHOICES = (
        ('male', 'MALE'),
        ('female', 'FEMALE'),
        ('unspecified', 'UNSPECIFIED'),
    )
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, db_index=True, primary_key=True
    )
    username = None
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True)
    personal_email = models.EmailField("email address", unique=True, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='/img')
    temporary_address = models.CharField(max_length=100, null=True, blank=True)
    permanent_address = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    alternate_phone_number = models.CharField(max_length=100, null=True, blank=True)
    joined_date = models.DateField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # last_login = None  (Uncomment this if you dont want last_login in the db table)
    USERNAME_FIELD = "email"  # make the user login with the email
    REQUIRED_FIELDS = []

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_staff

    def __str__(self):
        return self.first_name



# class BankDetails(models.Model):
#     bank_name = models.CharField(max_length=100, null=True, blank=True)
#     iifc_code = models.CharField(max_length=100, null=True, blank=True)
#     account_number = models.BigIntegerField(null=True, blank=True)
#     salary = models.IntegerField(null=True, blank=True)
#     is_active = models.BooleanField(default=True, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


# class ContactDetails(models.Model):
#     address = models.CharField(max_length=100, null=True, blank=True)
#     phone_number = models.CharField(max_length=100, null=True, blank=True)
#     is_active = models.BooleanField(default=True, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


# class Profile(models.Model):
#     GENDER_CHOICES = (
#         ('MALE', 'MALE'),
#         ('FEMALE', 'FEMALE'),
#         ('UNSPECIFIED', 'UNSPECIFIED'),
#     )
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     image = models.CharField(max_length=100, null=True, blank=True)
#     contact = models.ManyToManyField(ContactDetails)
#     temperory_address = models.CharField(max_length=100, null=True, blank=True)
#     permanent_address = models.CharField(max_length=100, null=True, blank=True)
#     phone_number = models.CharField(max_length=100, null=True, blank=True)
#     alternate_phone_number = models.CharField(max_length=100, null=True, blank=True)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     joined_date = models.DateField()
    # is_active = models.BooleanField(default=True, null=True, blank=True)
    # bank = models.ForeignKey(BankDetails, on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    # def __str__(self):
    #     return self.user.first_name