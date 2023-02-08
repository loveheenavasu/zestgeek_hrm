from django.db import models
from user_management.base import BaseModel
from multiselectfield import MultiSelectField


# Create your models here.
class Inventory(BaseModel):
    """
    Items inventory model
    """
    ITEM_CHOICE = (
        ("Laptop", "LAPTOP"), ("Monile", "MOBILE")
    )
    item = MultiSelectField(choices=ITEM_CHOICE, max_choices=3, max_length=10)
    LAPTOP_CHOICE = (
        ("Mac", "MAC"), ("Window", "WINDOW")
    )
    is_laptop = models.CharField(max_length=12, choices=LAPTOP_CHOICE, default="WINDOW")
    MOBILE_CHOICE = (
        ("IPhone", "IPHONE"), ("Android", "ANDROID")
    )
    is_mobile = models.CharField(max_length=12, choices=MOBILE_CHOICE, null=True, blank=True)
    title = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.item