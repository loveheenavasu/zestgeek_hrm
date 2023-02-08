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
    def post(self, request):
        item = request.POST.getlist('item')
        is_laptop = request.POST.get('is_laptop')
        if "Mobile" in item:
            is_mobile = request.POST.get('is_mobile')
        else:
            is_mobile = None
        title = request.POST.get('title')
        remarks = request.POST.get('remarks')
        Inventory.object.create(item=item, is_laptop=is_laptop, is_mobile=is_mobile, title=title, remarks=remarks)
        messages.success(request, "Inventory created successfully.")
        print("successful")
        return redirect("inventory")
