from django.urls import path
from inventory.views import *

urlpatterns = [
    path('inventory/<id>', InventoryView.as_view(), name='inventory'),



]