from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import *


# Create your views here.
class Register(View):
    def get(self, request):
        role = Role.objects.all()
        return render(request, "register.html", {"role":role})
    def post(self,request):
        print("abc")
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
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
            return redirect('/')

        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/')
        else:
            roles = Role.objects.get(role_name=role)
            dep = Department.objects.create(department_name=department)
            print(roles, "---------------------")
            CustomUser.objects.create_user(email=email, password=password1, role=roles, first_name=first_name, last_name=last_name, personal_email=personal_email
                                           , gender=gender, temperory_address=temperory_address, permanent_address=permanent_address, phone_number=phone_number,
                                           alternate_phone_number=alternate_phone_number, department=dep, joined_date=joined_date, image=image )

            messages.success(request, "Registeration successful.")
            print("successful")

            return redirect("/")
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



class Roles(View):
    def get(self, request):
        return render(request, 'roles.html')
    def post(self,request):
        role_name = request.POST.get('role_name')
        if Role.objects.filter(role_name=role_name).exists():
            messages.error(request, "Role already exists.")
            return redirect("roles")
        else:
            Role.objects.create(role_name=role_name)
            messages.success(request, "Role created successful.")
            return redirect("roles")
