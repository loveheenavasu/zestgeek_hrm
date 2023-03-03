from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import *
from user_management.models import Department,CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.http import JsonResponse
from utils import change_date, change_time
import json
from .leaves_validation import format_time, format_date, convert_time_to_hrs_minute, get_total_hours, convert_into_days,\
    validate_leaves
# Create your views here.

class EmployeeLeaves(LoginRequiredMixin, View):
    def get(self, request):
        leave_obj = Leaves.objects.filter(user=request.user.id)
        if leave_obj:
            remaining_leaves = sum([obj.remaining_leaves for obj in leave_obj])
        else:
            remaining_leaves = 18
        show_data = Leaves.objects.all()
        dept = Department.objects.all()
        print(remaining_leaves, "remaining_leave--------")
        return render(request, 'leave.html', {'show_data': show_data, 'dept': dept, "remaining_leave":remaining_leaves})
    def post(self, request):
        try:
            # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if request.method == 'POST':
                print(request.POST, "-----------------------------------------")
                data = json.loads(request.body)
                print(data, "====")
                start_date = request.POST.getlist('start_date')
                leaves_list = data.get("leaves")
                department = data.get("department")
                comments = data.get("comments")
                reason = data.get("reason")
                user_obj = CustomUser.objects.get(id=request.user.id)
                dept_obj = Department.objects.get(department_name=department)
                remaining_leaves = data.get("remaining_leaves")
                attachments = data.get("attachments")

                leaves_date_list = []
                leave_details = []
                for obj in leaves_list:
                    leaves_date_list.append(format_date(obj.get("startDate")))
                    leave_details.append({"leave_type": obj.get("leaveType"),
                                          "start_date": format_date(obj.get("startDate")),
                                          "start_time": format_time(obj.get("startTime")),
                                          "end_time": format_time(obj.get("endTime"))
                                          })
                start_date = min(leaves_date_list)
                end_date = max(leaves_date_list)

                check, data_or_message = validate_leaves(leaves_list, remaining_leaves)
                if check:
                    emp_leave = Leaves.objects.create(user=user_obj, dept_name=dept_obj,
                                                      start_date=start_date,
                                                      end_date=end_date,
                                                      reason=reason,
                                                      remaining_leaves=data_or_message,
                                                      attachments=attachments,
                                                      comments=comments,
                                                      days=len(leaves_date_list))

                    leave_details = [LeavesDetails(**obj, leave=emp_leave) for obj in leave_details]
                    LeavesDetails.objects.bulk_create(leave_details)

                    messages.success(request, "Leave applied successfully.")
                    return JsonResponse({'message': data_or_message})
                    # return redirect("/employee_leaves")
                else:
                    return JsonResponse({'message': data_or_message})
        except Exception as e:
            print(e)
class EmployeeProfile(LoginRequiredMixin, View):
    def get(self, request):
        user_id = request.user.id
        print(user_id, "user_id")
        show_data = CustomUser.objects.get(id=user_id)
        print(show_data, "show_data")
        return render(request, 'profile-detail.html', {'show_data': show_data})
