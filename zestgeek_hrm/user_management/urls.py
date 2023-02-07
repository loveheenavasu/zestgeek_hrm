from django.urls import path
from user_management.views import *
from . import views
urlpatterns = [
    # path('', Register.as_view()),
    # path('employee', Employee.as_view())
    path("", views.register, name="register"),
    path("login", views.login_user, name="login"),

]