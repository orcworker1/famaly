from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.db import transaction
from .models import Household, FamilyMember


@transaction.atomic
def create_household(*, user, name, currency="RUB"):
    hh = Household.objects.create(name=name, currency=currency, created_by=user)
    FamilyMember.objects.create(household=hh, user=user, role=FamilyMember.Role.OWNER)
    return hh


class ViewExpenses(TemplateView):
    template_name = 'index.html'


# Create your views here.
