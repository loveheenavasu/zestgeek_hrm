from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
import json

# Create your views here.
class Register(LoginRequiredMixin, View):
    def get(self, request):
        role = Role.objects.all()
        department = Department.objects.all()
        return render(request, "register.html", {"role": role, "department": department})

    def post(self, request):
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
            return redirect('/register')

        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
        else:
            roles = Role.objects.get(role_name=role)
            dep = Department.objects.get(department_name=department)
            CustomUser.objects.create_user(email=email, password=password, role=roles, first_name=first_name,
                                           last_name=last_name, personal_email=personal_email
                                           , gender=gender, temporary_address=temporary_address,
                                           permanent_address=permanent_address, phone_number=phone_number,
                                           alternate_phone_number=alternate_phone_number, department=dep,
                                           joined_date=joined_date, image=image)

            messages.success(request, "Registration successful.")
            print("successful")

            return redirect("/home")


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/home')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successfully")
            return redirect('/home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('/')


class Roles(LoginRequiredMixin, View):
    def get(self, request):
        role = Role.objects.all()
        return render(request, 'role.html', {"roles": role})

    def post(self, request):
        role_name = request.POST.get('role_name')
        if Role.objects.filter(role_name=role_name).exists():
            messages.error(request, "Role already exists.")
            return redirect("/roles")
        else:
            Role.objects.create(role_name=role_name)
            messages.success(request, "Role created successful.")
            return redirect("/roles")


class UpdateRole(LoginRequiredMixin, View):
    def get(self, request, id):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            ids = request.GET['id']
            role = Role.objects.get(id=ids)
            return HttpResponse(role)
        role = Role.objects.get(id=id)
        return render(request, 'role.html', {"role": role})

    def post(self, request, id):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            idss = request.POST["emp_id"]
            name = request.POST["name"]
            role = Role.objects.get(id=idss)
            role.role_name = name
            role.save()
            messages.success(request, "Role updated successful.")
            return HttpResponse("Role updated successful.")
        return redirect("/roles")


class DeleteRole(LoginRequiredMixin, View):
    def get(self, request, id):
        role = Role.objects.get(id=id)
        role.delete()
        messages.success(request, "role deleted successful.")
        return redirect("/roles")


class DepartmentView(LoginRequiredMixin, View):
    def get(self, request):
        departments = Department.objects.all()
        result = {}
        user_depart = CustomUser.objects.select_related('department').filter(is_admin=False)
        for user in user_depart:
            if user.department.department_name not in result:
                result[user.department.department_name] = {user.department_id: [user.image.url]}
            else:
                result[user.department.department_name][user.department_id].append(user.image.url)
        for department in departments:
            if department.department_name not in result:
                result[department.department_name] = {department.id: [None]}
        return render(request, 'employee-team.html', {'result': result})

    def post(self, request):
            department_name = request.POST.get('department_name')
            if not Department.objects.filter(department_name=department_name).exists():
                Department.objects.create(department_name=department_name)
                messages.success(request, "Department created successful.")
                return redirect("/department")
            else:
                messages.error(request, "Department already exists.")
                return redirect("/department")

        # else:
        #     Department.objects.create(department_name=department_name)
        #     messages.success(request, "Department created successful.")
        #     return redirect("department")


class UpdateDepartment(LoginRequiredMixin, View):
    def get(self, request,id):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            ids = request.GET['id']
            depp = Department.objects.get(id=ids)
            return HttpResponse(depp)
        depp = Department.objects.get(id=id)
        return render(request, 'employee-team.html', {'depp':depp})

    def post(self, request, id):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            idss = request.POST["emp_id"]
            name = request.POST["name"]
            if not Department.objects.filter(department_name=name).exists():
                Department.objects.filter(id=idss).update(department_name=name)
                messages.success(request, "Department updated successful.")
                return HttpResponse("Department updated successful.")
            else:
                messages.error(request, "Department already exists.")
                return redirect("/department")
        return redirect("department")

class DeleteDepartment(LoginRequiredMixin, View):
    def get(self, request, id):
        department = Department.objects.get(id=id)
        department.delete()
        messages.success(request, "Department deleted successful.")
        return redirect("department")


class EmployeeView(LoginRequiredMixin, View):
    def get(self, request):
        user = CustomUser.objects.filter(is_admin=False)
        total_employee = user.count()
        role = Role.objects.all()
        department = Department.objects.all()
        return render(request, 'employee.html',
                      {"user": user, "total_employee": total_employee, "role": role,
                       "department": department})

    def post(self, request):
        print("In function")
        current_user = request.user.first_name
        user = CustomUser.objects.all()
        total_employee = user.count()
        role = Role.objects.all()
        department = Department.objects.all()
        # form = RegisterForm(request.POST, request.FILES)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST:
            print("request.post", request.POST)
        # if request.is_ajax() and request.method == "POST":
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
            image = request.FILES.get('image')
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'status': 'Error', 'message': "Email already exists"})
            if CustomUser.objects.filter(personal_email=personal_email).exists():
                return JsonResponse({'status': 'Error', 'message': "Personal email already exists"})
            if password != confirm_password:
                return JsonResponse({'status': 'Error', 'message': "Password doesn't not matched"})
            roles = Role.objects.get(role_name=role)
            dep = Department.objects.get(department_name=department)
            obj = CustomUser.objects.create_user(email=email, password=password, role=roles, first_name=first_name,
                                                 last_name=last_name, personal_email=personal_email
                                                 , gender=gender, temporary_address=temporary_address,
                                                 permanent_address=permanent_address, phone_number=phone_number,
                                                 alternate_phone_number=alternate_phone_number, department=dep,
                                                 joined_date=joined_date, image=image)

            obj.save()
            messages.success(request, "Employee created successfully")
            print("successful")
            return JsonResponse({'status': 'Success', 'message': "Employee created successfully"})

        else:
            return render(request, "employee.html",
                          {"user": user, "total_employee": total_employee, "current_user": current_user,
                           "role": role, "department": department})

class UpdateEmployee(View):
    def get(self, request, id):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            ids = request.GET['id']
            user = CustomUser.objects.get(id=ids)

            return JsonResponse({"first_name":user.first_name,"email":user.email, "password":user.password, "role":user.role.role_name,
                                                 "last_name":user.last_name, "personal_email":user.personal_email
                                                 , "gender":user.gender, "temporary_address":user.temporary_address,
                                                 "permanent_address":user.permanent_address, "phone_number":user.phone_number,
                                                 "alternate_phone_number":user.alternate_phone_number, "department":user.department.department_name,
                                                 "joined_date":user.joined_date, "image":user.image.path})
        return render(request, 'employee-team.html')

    def post(self, request, id):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("i am in")
            idss = request.POST["id"]
            email = request.POST.get('email')
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
            roles = Role.objects.get(role_name=role)
            dep = Department.objects.get(department_name=department)
            user = CustomUser.objects.get(id=idss)
            if request.FILES.get('image'):
                user.image= request.FILES.get('image')
            else:
                user.image=user.image
            user.joined_date = joined_date
            user.department = dep
            user.alternate_phone_number = alternate_phone_number
            user.phone_number = phone_number
            user.permanent_address = permanent_address
            user.temporary_address = temporary_address
            user.gender = gender
            user.personal_email = personal_email
            user.role = roles
            user.last_name = last_name
            user.first_name = first_name
            user.email = email
            user.password= user.password
            user.save()
            messages.success(request, "Employee updated successfully")
            return JsonResponse({'message':"Employee updated successfully"})
        
        return redirect("department")

class DeleteEmployee(LoginRequiredMixin, View):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        user.delete()
        messages.success(request, "Employee deleted successful.")
        return JsonResponse({'message':"Employee deleted successful."})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def home(request):
    return render(request, 'index.html')


@login_required
def employee_index(request):
    return render(request, 'index-employee.html')
