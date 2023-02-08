from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login


# Create your views here.
class Register(View):
    def get(self, request):
        role = Role.objects.all()
        department = Department.objects.all()
        return render(request, "register.html", {"role": role, "department": department})

    def post(self, request):
        print("abc")
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        personal_email = request.POST.get('personal_email')
        gender = request.POST.get('gender')
        temporary_address = request.POST.get('temporary_address')
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

        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/')
        else:
            roles = Role.objects.get(role_name=role)
            dep = Department.objects.get(department_name=department)
            print(roles, "---------------------")
            CustomUser.objects.create_user(email=email, password=password, role=roles, first_name=first_name,
                                           last_name=last_name, personal_email=personal_email
                                           , gender=gender, temporary_address=temporary_address,
                                           permanent_address=permanent_address, phone_number=phone_number,
                                           alternate_phone_number=alternate_phone_number, department=dep,
                                           joined_date=joined_date, image=image)

            messages.success(request, "Registration successful.")
            print("successful")

            return redirect("/employee")


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/register')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('/login')


class Roles(View):
    def get(self, request):
        role = Role.objects.all()
        return render(request, 'roles.html', {"role": role})

    def post(self, request):
        role_name = request.POST.get('role_name')
        if Role.objects.filter(role_name=role_name).exists():
            messages.error(request, "Role already exists.")
            return redirect("roles")
        else:
            Role.objects.create(role_name=role_name)
            messages.success(request, "Role created successful.")
            return redirect("roles")


class UpdateRole(View):
    def get(self, request, id):
        role = Role.objects.get(id=id)
        return render(request, 'roles.html', {"role": role})

    def post(self, request, id):
        name = request.POST.get("role_name")
        role = Role.objects.get(id=id)
        role.role_name = name
        role.save()
        messages.success(request, "Role updated successful.")
        return redirect("roles")


class DeleteRole(View):
    def get(self, request, id):
        role = Role.objects.get(id=id)
        role.delete()
        messages.success(request, "role deleted successful.")
        return redirect("roles")


class DepartmentView(View):
    def get(self, request):
        department = Department.objects.all()
        return render(request, 'department.html', {"department": department})

    def post(self, request):
        department_name = request.POST.get('department_name')
        if Department.objects.filter(department_name=department_name).exists():
            messages.error(request, "Department already exists.")
            return redirect("department")
        else:
            Department.objects.create(department_name=department_name)
            messages.success(request, "Department created successful.")
            return redirect("department")


class UpdateDepartment(View):
    def get(self, request, id):
        department = Department.objects.get(id=id)
        return render(request, 'department.html', {"department": department})

    def post(self, request, id):
        name = request.POST.get("department_name")
        department = Department.objects.get(id=id)
        department.department_name = name
        department.save()
        messages.success(request, "Department updated successful.")
        return redirect("department")


class DeleteDepartment(View):
    def get(self, request, id):
        department = Department.objects.get(id=id)
        department.delete()
        messages.success(request, "Department deleted successful.")
        return redirect("department")


class EmployeeView(View):
    def get(self, request):
        return render(request, 'employee.html')
