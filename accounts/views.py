from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import FormView
from django.contrib.auth.views import LogoutView


class MyLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы вышли из аккаунта")
        return super().dispatch(request, *args, **kwargs)



class SignUpView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Регистрация прошла успешно!")
        return super().form_valid(form)

# Create your views here.

