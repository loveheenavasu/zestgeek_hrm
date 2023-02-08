from django.urls import path
from user_management.views import *

urlpatterns = [
    path('', Register.as_view()),
    path('roles', Roles.as_view()),
    path('login', LoginView.as_view()),
    path('department', DepartmentView.as_view()),
    path('employee', EmployeeView.as_view())



]