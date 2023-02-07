from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import *


# Create your views here.
class Register(View):
    def get(self, request):
        return render(request, "register.html")
    def post(self,request):
        print("abc")
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        personal_email = request.POST.get('personal_email')
        gender = request.POST.get('gender')
        temperory_address = request.POST.get('temperory_address')
        permanent_address = request.POST.get('permanent_address')
        phone_number = request.POST.get('phone_number')
        alternate_phone_number = request.POST.get('alternate_phone_number')
        department = request.POST.get('department')
        joined_date = request.POST.get('joined_date')
        image = request.FILES.get("image")

        if CustomUser.objects.filter(email=email).exists():
            print("already exists")
            messages.error(request, "Email already exists")
            return render(request, "register.html")
            # return redirect("/")
        else:
            CustomUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, role=role, personal_email=personal_email
                                           , gender=gender, temperory_address=temperory_address, permanent_address=permanent_address, phone_number=phone_number,
                                           alternate_phone_number=alternate_phone_number, department=department, joined_date=joined_date, image=image )
            messages.success(request, "Registeration successful.")
            print("successful")

            return redirect("register")


class Employee(View):
    def get(self, request):
        pass
    def post(self,request):
        pass