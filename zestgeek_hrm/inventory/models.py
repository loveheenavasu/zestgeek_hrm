from django.db import models
import uuid


# Create your models here.
class Inventory(models.Model):
    """
    Items inventory model
    """
    inventory_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    ITEM_CHOICE = (
        ("LAPTOP", "LAPTOP"), ("MOBILE", "MOBILE")
    )
    item = models.CharField(max_length=12, choices=ITEM_CHOICE, default="LAPTOP")
    LAPTOP_CHOICE = (
        ("MAC", "MAC"), ("WINDOW", "WINDOW")
    )
    is_laptop = models.CharField(max_length=12, choices=LAPTOP_CHOICE, default="WINDOW")
    MOBILE_CHOICE = (
        ("IPHONE", "IPHONE"), ("ANDROID", "ANDROID")
    )
    is_mobile = models.CharField(max_length=12, choices=MOBILE_CHOICE, default="ANDROID")
    title = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
