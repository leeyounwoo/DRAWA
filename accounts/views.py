from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm


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


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, username):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


# @login_required
# @require_http_methods(['GET', 'POST'])
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#             return redirect('articles:index')
#     else:
#         form = PasswordChangeForm(request.user)
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/change_password.html', context)


def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)



def calander(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    # shoes = get_object_or_404(Product, pk=shoes_pk)
    # draw = shoes.draw_set.all()

    # # 이미 예약 해놨다면 -> 취소
    # if draw.reservation.filter(pk=request.user.pk).exists():
    #     draw.reservation.remove(request.user)
    # # 예약
    # else:
    #     draw.reservation.add(request.user)
    
    # return redirect('drawa:shoes_detail')


def interest(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    # shoes = get_object_or_404(Product, pk=shoes_pk)

    # # 이미 관심 등록 해놨다면 -> 취소
    # if shoes.wishlist.filter(pk=request.user.pk).exists():
    #     shoes.wishlist.remove(request.user)
    # # 관심 등록
    # else:
    #     shoes.wishlist.add(request.user)
    
    # # 그 전에 있던 페이지로 이동
    # return redirect('drawa:shoes_detail')
    # # return redirect('drawa:index')