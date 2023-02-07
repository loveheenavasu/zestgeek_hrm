from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import *

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
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
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')


        if password == confirm_password:
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect('/register')
            # elif User.objects.filter(email=email).exists():
            #     messages.info(request, 'Email is already taken')
            #     return redirect('/register')
            else:
                user = CustomUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, role=role, personal_email=personal_email, gender=gender, temperory_address=temperory_address, permanent_address=permanent_address, phone_number=phone_number,
                                           alternate_phone_number=alternate_phone_number, department=department, joined_date=joined_date, image=image)
                messages.info(request, 'User Created Successfully')
                user.save()
                return redirect('/login')
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect('/register')
    else:
        return render(request, 'register.html')

# Create your views here.
# class Register(View):
#     def get(self, request):
#         return render(request, "register.html")
#     def post(self,request):
#         print("abc")
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         role = request.POST.get('role')
#         personal_email = request.POST.get('personal_email')
#         gender = request.POST.get('gender')
#         temperory_address = request.POST.get('temperory_address')
#         permanent_address = request.POST.get('permanent_address')
#         phone_number = request.POST.get('phone_number')
#         alternate_phone_number = request.POST.get('alternate_phone_number')
#         department = request.POST.get('department')
#         joined_date = request.POST.get('joined_date')
#         image = request.FILES.get("image")
#
#         if CustomUser.objects.filter(email=email).exists():
#             print("already exists")
#             messages.error(request, "Email already exists")
#             return render(request, "register.html")
#             # return redirect("/")
#         else:
#             CustomUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, role=role, personal_email=personal_email
#                                            , gender=gender, temperory_address=temperory_address, permanent_address=permanent_address, phone_number=phone_number,
#                                            alternate_phone_number=alternate_phone_number, department=department, joined_date=joined_date, image=image )
#             messages.success(request, "Registeration successful.")
#             print("successful")
#
#             return redirect("register")

def login_user(request, *args, **kwargs):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/register')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('/login')
    else:
        return render(request, 'login.html')



class Employee(View):
    def get(self, request):
        pass
    def post(self,request):
        pass