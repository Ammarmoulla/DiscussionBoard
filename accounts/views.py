from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import *
# Create your views here.
def signup(request):
    context = {}
    form = SipnUpForm()
    if request.method == "POST":
        form = SipnUpForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context=context)
