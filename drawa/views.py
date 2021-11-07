from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .models import Product, Store

@require_safe
def index(request):
    products = Product.objects.all()
    
    context = {
        'products': products,
    }
    return render(request, 'drawa/index.html', context)


@require_safe
def detail(request, shoes_pk):
    # 디테일 페이지에 해당 하는 신발
    shoes = get_object_or_404(Product, pk=shoes_pk)
    # 해당하는 신발의 드로우 정보
    draw = shoes.draw_set.all()
    # 드로우에 해당하는 스토어 정보 (이게 가능할까?)
    store = draw.store

    context = {
        'shoes': shoes,
        'draw': draw,
        'store': store, 
    }
    return render(request, 'drawa/detail.html', context)


@login_required
@require_safe
def place(request):
    stores = Store.objects.all()

    context = {
        'stores': stores,
    }
    return render(request, 'drawa/place.html', context)


@require_POST
def shoes_reservation(request, shoes_pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    shoes = get_object_or_404(Product, pk=shoes_pk)
    draw = shoes.draw_set.all()

    # 이미 예약 해놨다면 -> 취소
    if draw.reservation.filter(pk=request.user.pk).exists():
        draw.reservation.remove(request.user)
    # 예약
    else:
        draw.reservation.add(request.user)
    
    return redirect('drawa:shoes_detail')


@require_POST
def interesting(request, shoes_pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    shoes = get_object_or_404(Product, pk=shoes_pk)

    # 이미 관심 등록 해놨다면 -> 취소
    if shoes.wishlist.filter(pk=request.user.pk).exists():
        shoes.wishlist.remove(request.user)
    # 관심 등록
    else:
        shoes.wishlist.add(request.user)
    
    # 그 전에 있던 페이지로 이동
    return redirect('drawa:shoes_detail')
    # return redirect('drawa:index')