from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import *
from user_management.models import Department,CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.http import JsonResponse
from utils import change_date, change_time
# Create your views here.

# def change_date(date):
#     changed_date = datetime.strptime(date, '%Y-%m-%d').date()
#     return changed_date

class EmployeeLeaves(LoginRequiredMixin,View):
    def get(self, request):
        show_data = Leaves.objects.all()
        dept = Department.objects.all()
        return render(request, 'leave.html', {'show_data': show_data, 'dept': dept})
    def post(self, request):
        try:
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
                start_time = request.POST.getlist('start_time')
                end_time = request.POST.getlist('end_time')
                user_id = request.user.id
                userr = CustomUser.objects.get(id=user_id)
                dept_name = request.POST.get('department')
                name_dept = Department.objects.get(department_name=dept_name)
                emp_leave = Leaves.objects.create(user=userr,dept_name=name_dept, start_date=change_date(start_date[0]), end_date=change_date(end_date[-1]), reason=reason, remaining_leaves=remaining_leaves,
                                                  attachments=attachments, comments=comments, days=(change_date(end_date[-1])-change_date(start_date[0])).days)

                result = []
                for i in range(len(start_date)):
                    if start_date[i] == '':
                        start_date[i] = None
                    elif end_date[i] == '':
                        end_date[i] = None
                    elif start_time[i] == '':
                        start_time[i] = None
                    elif end_time[i] == '':
                        end_time[i] = None
                    leave_details = LeavesDetails(
                        leave=emp_leave,
                        leave_type=leave_type[i],
                        start_date=change_date(start_date[i]) if start_date[i] else start_date[i],
                        end_date=change_date(end_date[i]) if end_date[i] else end_date[i],
                        start_time=change_time(start_time[i]) if start_time[i] else start_time[i],
                        end_time=change_time(start_time[i]) if start_time[i] else start_time[i])
                    result.append(leave_details)
                LeavesDetails.objects.bulk_create(result)
                messages.success(request, "Leave applied successfully.")
                return JsonResponse({'message':"successfully"})
            return redirect("/employee_leaves")
        except Exception as e:
            print(e)
class EmployeeProfile(LoginRequiredMixin,View):
    def get(self, request):
        user_id = request.user.id
        print(user_id, "user_id")
        show_data = CustomUser.objects.get(id=user_id)
        print(show_data, "show_data")
        return render(request, 'profile-detail.html', {'show_data': show_data})