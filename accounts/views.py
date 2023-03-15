from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.models import User
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


class ProfileUpdateView(UpdateView):
    model = User
    fields = ("first_name", "last_name", "email")
    template_name = "accounts/my_account.html"
    success_url = reverse_lazy("my_account")

    def get_object(self):
        return self.request.user