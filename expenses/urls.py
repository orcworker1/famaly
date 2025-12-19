from django.contrib import admin
from django.urls import path , include
from expenses.views import ViewExpenses

urlpatterns = [
    path('', ViewExpenses.as_view(), name='index'),
]