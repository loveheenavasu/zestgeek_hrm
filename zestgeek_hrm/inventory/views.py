from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import *
from user_management.models import CustomUser


# Create your views here.
class InventoryView(View):
    def get(self, request, id):
        employee = CustomUser.objects.get(id=id)
        return render(request, 'add-inventory.html', {"employee": employee})

    def post(self, request, id):
        item = request.POST.getlist('item')
        print(item, '------------')
        is_laptop = request.POST.get('is_laptop')
        print(is_laptop, '============')
        if "Mobile" in item:
            is_mobile = request.POST.get('is_mobile')
        else:
            is_mobile = None
        title = request.POST.get('title')
        remarks = request.POST.get('remarks')
        create_inventory = Inventory.objects.create(item=item, is_laptop=is_laptop, is_mobile=is_mobile, title=title, remarks=remarks)
        userr = CustomUser.objects.get(id=id)
        userr.inventory = create_inventory
        userr.save()
        messages.success(request, "Inventory created successfully.")
        print("successful")
        return redirect("/employee")

class ListingInventory(View):
    def get(self, request):
        user_inventory = CustomUser.objects.all()
        return render(request, "inventory.html", {"data": user_inventory})