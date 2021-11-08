from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .models import Draw, Product, Store
from datetime import datetime
from pytz import timezone

@require_safe
def index(request):
    # 현재시간
    now_time = datetime.now(timezone('Asia/Seoul'))

    # 드로우 정보 가져오기
    now = Draw.objects.filter(start__lte=now_time, end__gt=now_time)
    upcoming = Draw.objects.filter(start__gt=now_time)

    # 드로우에서 product에 접근
    # 현재 진행 중인 드로우
    now_products = []
    now_draws = {}
    for draw in now:
        now_products.append(draw.product)

        if draw.product.pk in now_draws.keys():
            now_draws[draw.product.pk] = min(now_draws[draw.product.pk], draw.end)
        else:
            now_draws[draw.product.pk] = draw.end

    now_products = list(set(now_products)) # 중복제거

    # 진행 예정 드로우
    upcoming_products = []
    upcoming_draws = {}
    for draw in upcoming:
        upcoming_products.append(draw.product)

        if draw.product.pk in upcoming_draws.keys():
            upcoming_draws[draw.product.pk] = min(upcoming_draws[draw.product.pk], draw.start)
        else:
            upcoming_draws[draw.product.pk] = draw.start # end? start?

    upcoming_products = list(set(upcoming_products))

    # print(now_products)
    # print(upcoming_products)

    # print(now_draws)
    # print(upcoming_draws)


    context = {
        'now_products': now_products,
        'upcoming_products': upcoming_products,
        'now_draws': now_draws,
        'upcoming_draws': upcoming_draws,
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
    
    # 그 전에 있던 페이지로 이동
    return redirect('drawa:shoes_detail')
    # return redirect('drawa:index')



def favorite(request):
    context = {
        
    }
    return render(request, 'drawa/favorite.html', context)

