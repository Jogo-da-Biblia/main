from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from app.core.serializers import CustomTokenObtainPairSerializer

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from rest_framework import status
from rest_framework.response import Response

from .validations import validate_email

from .exceptions import *

from .forms import NewUserForm
from django.contrib.auth import get_user_model


User = get_user_model()

def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:homepage")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form})

    
    
