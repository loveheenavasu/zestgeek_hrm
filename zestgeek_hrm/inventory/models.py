from django.db import models
from zestgeek_hrm.user_management.models import CustomUser
import uuid


# Create your models here.
class Inventory(models.Model):
    """
    Items inventory model
    """
    inventory_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)
    item = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
