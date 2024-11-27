from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings

from . import forms

def login_page(request: HttpRequest) -> HttpResponse:
    """
    Handle user login.
    :param request:HTTP request Object
    :return: HTTP response rendering the login page with a form and message.
    """
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
    return render(request, 'authentication/login.html', context={'form': form, 'message': message})


def logout_user(request : HttpRequest) -> HttpResponse:
    """
    Log out the current user.
    :param request:HTTP request object.
    :return: HTTP response redirecting to the login page.
    """
    logout(request)
    return redirect('login')

def signup_page(request : HttpRequest) -> HttpResponse:
    """
    Handle user registration.
    :param request: HTTP request object.
    :return: HTTP response rendering the signup page with a form.
    """
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})
