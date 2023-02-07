from django.urls import path
from user_management.views import *

urlpatterns = [
    path('register/', Register.as_view()),
    path('employee/', Employee.as_view())


]