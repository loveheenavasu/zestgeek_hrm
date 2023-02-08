from django.urls import path
from user_management.views import *
from . import views
urlpatterns = [
    path('', Register.as_view()),
    path('roles', Roles.as_view()),
    path('update_role/<id>', UpdateRole.as_view()),
    path('delete_role/<id>', DeleteRole.as_view()),
    path('login', LoginView.as_view()),
    path('department', DepartmentView.as_view()),
    path('update_department/<id>', UpdateDepartment.as_view()),
    path('delete_department/<id>', DeleteDepartment.as_view()),
    path('employee', EmployeeView.as_view()),
    path('logout', views.logout)
]