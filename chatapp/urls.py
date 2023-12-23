from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.index, name='index'),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("home1", views.home1, name="home1"),
    path("create-total-budget/", CreateTotalBudget.as_view()),
    path("get-total-budget/", GetTotalBudget.as_view()),
    path("create-daily-expance/", CreateDailyExpance.as_view()),
    path("get-daily-expance/", GetDailyExpance.as_view()),
]