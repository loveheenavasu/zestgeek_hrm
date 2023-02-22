from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import *
from user_management.models import Department,CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class EmployeeLeaves(LoginRequiredMixin,View):
    def get(self, request):
        show_data = Leaves.objects.all()
        return render(request, 'leave.html', {'show_data': show_data})
    def post(self, request):
        dept_name = request.POST.get('dept_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        remaining_leaves = request.POST.get('remaining_leaves')
        attachments = request.FILES.get('attachments')
        comments = request.POST.get('comments')
        leave_type = request.POST.get('leave_type')
        user_id = request.user.id
        userr = CustomUser.objects.get(id=user_id)
        name_dept = Department.objects.get(dept_name=dept_name)
        emp_leave = Leaves.objects.create(user=userr,dept_name=name_dept, start_date=start_date, end_date=end_date, reason=reason, remaining_leaves=remaining_leaves,
                                          attachments=attachments, comments=comments)
        LeavesDetails.objects.create(leave=emp_leave, leave_type=leave_type)
        messages.success(request, "Leave applied successfully.")
        return redirect("/leave")

class EmployeeProfile(LoginRequiredMixin,View):
    def get(self, request):
        user_id = request.user.id
        print(user_id, "user_id")
        show_data = CustomUser.objects.get(id=user_id)
        print(show_data, "show_data")
        return render(request, 'profile-detail.html', {'show_data': show_data})