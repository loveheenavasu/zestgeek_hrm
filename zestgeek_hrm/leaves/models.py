from django.db import models
import uuid
from user_management.models import Department
# from user_management.models import Department, Profile
# Create your models here.
class Leaves(models.Model):
    leave_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    dept_name = models.ForeignKey(Department, on_delete=models.DO_NOTHING)

    STATUS_CHOICE = (
        ("ACCEPTED", "ACCEPTED"), ("PENDING", "PENDING"), ("CANCELLED", "CANCELLED"), ("PARTIALACCEPTED", "PARTIALACCEPTED")
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="PENDING")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=200)
    remaining_leaves = models.IntegerField()
    attachments = models.CharField(max_length=200, null=True, blank=True)
    comments = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approval_by = models.CharField(max_length=200, null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)

class LeavesDetails(models.Model):
    leave_details_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    leave = models.ForeignKey(Leaves, on_delete=models.DO_NOTHING)
    TYPE_CHOICE = (
        ("FULLDAY", "FULLDAY"), ("HALFDDAY", "HALFDAY"), ("SHORTLEAVE", "SHORTLEAVE")
    )
    leave_type = models.CharField(max_length=10, choices=TYPE_CHOICE, default="FULLDAY")
    STATUS_CHOICE = (
        ("ACCEPTED", "ACCEPTED"), ("PENDING", "PENDING"), ("CANCELLED", "CANCELLED")
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICE, default="PENDING")
    from_date = models.DateField(auto_now=False)
    to_date = models.DateField(auto_now=False)
    days = models.IntegerField()


