from django.urls import path
from inventory.views import *

urlpatterns = [
    path('inventory/<id>', InventoryView.as_view(), name='inventory'),
    path('listing_inventory', ListingInventory.as_view(), name='listing_inventory'),



]