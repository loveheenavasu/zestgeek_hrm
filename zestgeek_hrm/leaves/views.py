from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import *
from user_management.models import Department,CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.http import JsonResponse

# Create your views here.


class EmployeeLeaves(LoginRequiredMixin,View):
    def get(self, request):
        show_data = Leaves.objects.all()
        dept = Department.objects.all()
        return render(request, 'leave.html', {'show_data': show_data, 'dept': dept})
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print(request.POST, "-----------------------------------------")
            start_date = request.POST.getlist('start_date')
            end_date = request.POST.getlist('end_date')
            print(start_date, "-----------------")
            reason = request.POST.get('reason')
            remaining_leaves = 11
            attachments = request.FILES.get('attachments')
            comments = request.POST.get('comments')
            leave_type = request.POST.getlist('leave_type')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            if start_time == '':
                start_time=None
            else:
                start_time=start_time
            if end_time == '':
                end_time =None
            else:
                end_time =end_time
            user_id = request.user.id
            userr = CustomUser.objects.get(id=user_id)
            dept_name = request.POST.get('department')
            name_dept = Department.objects.get(department_name=dept_name)
            emp_leave = Leaves.objects.create(user=userr,dept_name=name_dept, start_date=start_date, end_date=end_date, reason=reason, remaining_leaves=remaining_leaves,
                                              attachments=attachments, comments=comments,start_time=start_time,end_time=end_time)
            LeavesDetails.objects.create(leave=emp_leave, leave_type=leave_type,start_date=start_date, end_date=end_date,days=(end_date-start_date).days)
            messages.success(request, "Leave applied successfully.")
            return JsonResponse({'message':"successfully"})
        return redirect("/employee_leaves")

class EmployeeProfile(LoginRequiredMixin,View):
    def get(self, request):
        user_id = request.user.id
        print(user_id, "user_id")
        show_data = CustomUser.objects.get(id=user_id)
        print(show_data, "show_data")
        return render(request, 'profile-detail.html', {'show_data': show_data})