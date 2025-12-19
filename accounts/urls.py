from django.contrib import admin
from django.urls import path
from django.urls import include
from .import views
from .views import SignUpView
from .views import MyLogoutView

urlpatterns = [
    path('signup/',SignUpView.as_view(), name='signup'),
    path('logout',MyLogoutView.as_view(), name='logout' )

]
