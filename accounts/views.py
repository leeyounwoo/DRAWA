from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm


User = get_user_model()

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('drawa:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'drawa:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('drawa:index')


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('drawa:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('drawa:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_POST
def quit(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('drawa:index') 


@require_safe
def profile(request, username):
    profile = get_object_or_404(User, username=username)
    context = {
        'profile': profile, 
    }
    return render(request, 'accounts/profile.html', context)


@require_safe
def calander(request, username):
    profile = get_object_or_404(User, username=username)
    
    context = {
        'profile': profile, 
        
    }
    return render(request, 'accounts/calander.html', context)


@require_safe
def interest(request, username):
    profile = get_object_or_404(User, username=username)
    
    context = {
        'profile': profile, 
        
    }
    return render(request, 'accounts/interest.html', context)