from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .models import Product, Store, Draw

@require_safe
def index(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'drawa/index.html', context)


@require_safe
def detail(request, shoes_pk):
    product = get_object_or_404(Product, pk=shoes_pk)

    draws = product.draw_set.all()

    # 1번째 방법: filter 사용
    # temp = draws.filter(can_delivery = True) # ==> (속성) 가능
    # temp = draws.filter(store__nation='korea') # ==> (외래키.속성) 불가능
    # print(temp)

    # 2번째 방법: for문 + 쿼리셋 합치기
    korea_can_delivery = []
    korea_not_delivery = []
    abroad_direct = []
    abroad_not_direct = []
    for draw in draws:
        if draw.store.nation == 'korea':
            if draw.can_delivery == True:
                print('국내_온라인', draw)
                korea_can_delivery.append(draw)
            else:               
                print('국내_오프라인', draw)
                korea_not_delivery.append(draw)
        else:
            if draw.is_direct:
                print('직배송', draw)
                abroad_direct.append(draw)
            else:
                print('직배송 X', draw)
                abroad_not_direct.append(draw)



    context = {
        'product': product,
        'korea_can_delivery': korea_can_delivery,
        'korea_not_delivery': korea_not_delivery,
        'abroad_direct': abroad_direct,
        'abroad_not_direct': abroad_not_direct,
    }
    return render(request, 'drawa/detail.html', context)


# @login_required
# @require_safe
# def place(request):
#     stores = Store.objects.all()

#     context = {
#         'stores': stores,
#     }
#     return render(request, 'drawa/place.html', context)


# @require_POST
# def shoes_reservation(request, shoes_pk):
#     if not request.user.is_authenticated:
#         return redirect('accounts:login')
    
#     shoes = get_object_or_404(Product, pk=shoes_pk)
#     draw = shoes.draw_set.all()

#     # 이미 예약 해놨다면 -> 취소
#     if draw.reservation.filter(pk=request.user.pk).exists():
#         draw.reservation.remove(request.user)
#     # 예약
#     else:
#         draw.reservation.add(request.user)
    
#     return redirect('drawa:shoes_detail')


# @require_POST
# def interesting(request, shoes_pk):
#     if not request.user.is_authenticated:
#         return redirect('accounts:login')
    
#     shoes = get_object_or_404(Product, pk=shoes_pk)

#     # 이미 관심 등록 해놨다면 -> 취소
#     if shoes.wishlist.filter(pk=request.user.pk).exists():
#         shoes.wishlist.remove(request.user)
#     # 관심 등록
#     else:
#         shoes.wishlist.add(request.user)
    
#     # 그 전에 있던 페이지로 이동
#     return redirect('drawa:shoes_detail')
#     # return redirect('drawa:index')