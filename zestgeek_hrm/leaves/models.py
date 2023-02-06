from django.db import models
import uuid
from zestgeek_hrm.user_management.models import Profile, Department
# from user_management.models import Department, Profile
# Create your models here.


class Leaves(models.Model):
    leave_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    dept_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    TYPE_CHOICE = (
        ("FULLDAY", "FULLDAY"), ("HALFDDAY", "HALFDAY"), ("SHORTLEAVE", "SHORTLEAVE")
    )
    leave_type = models.CharField(max_length=10, choices=TYPE_CHOICE, default="FULLDAY")
    STATUS_CHOICE = (
        ("ACCEPTED", "ACCEPTED"), ("PENDING", "PENDING"), ("CANCELLED", "CANCELLED")
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICE, default="PENDING")
    start_date = models.DatField()
    end_date = models.DateField()
    reason = models.CharField(max_length=200)
    remaining_leaves = models.IntegerField()
    attachments = models.CharField(max_length=200, null=True, blank=True)
    comments = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

