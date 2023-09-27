from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render

from .forms import UserLoginForm, UserSignUpForm


def user_signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')  # Redirect to a home page or any other page
    else:
        form = UserSignUpForm()
    return render(request, 'reasonable_recommendation_app/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Use the authenticate function with the custom backend
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                # Specify the custom backend when calling the login function
                login(request, user, backend='reasonable_recommendation_app.backends.CustomUserAuthBackend')
                messages.success(request, 'Logged in successfully.')
                return redirect('home')  # Redirect to a home page or any other page
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = UserLoginForm()
    return render(request, 'reasonable_recommendation_app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')  # Redirect to a home page or any other page
