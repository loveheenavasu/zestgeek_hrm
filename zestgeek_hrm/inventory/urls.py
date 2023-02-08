from django.urls import path
from inventory.views import *

urlpatterns = [
    path('inventory', InventoryView.as_view()),



]