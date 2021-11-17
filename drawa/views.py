from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .models import Draw, Product, Store
from datetime import datetime, timedelta
from pytz import timezone
from django.http import JsonResponse, HttpResponse
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from django.utils import timezone as tz
# from selenium import webdriver as wd 
import time 
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.response import Response

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
    now_products.sort(key=lambda x: now_draws[x.pk]) # 시간순 정렬
    # 터무니없는 항목 제거
    limit_time = now_time + timedelta(weeks=520) # 10년 안에 드로우가 안끝나면 거짓 정보로 판단
    while len(now_products) > 0:
        if now_draws[now_products[-1].pk] > limit_time:
            now_products.pop()
        else:
            break

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
    upcoming_products.sort(key=lambda x: upcoming_draws[x.pk])

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
    # 현재시간
    now_time = datetime.now(timezone('Asia/Seoul'))

    # 드로우 정보 가져오기
    # 진행중: 시작시간 <= 현재 시간 <= 종료시간
    proceeding_draws = product.draw_set.filter(start__lte=now_time, end__gte=now_time)
    # 진행예정: 시작시간 > 현재 시간
    upcoming_draws = product.draw_set.filter(start__gt=now_time)
    # 종료: 종료시간 < 현재 시간
    finished_draws = product.draw_set.filter(end__lte=now_time)

    # 진행중
    korea_can_delivery_proceeding_draws = []
    korea_not_delivery_proceeding_draws = []
    abroad_direct_proceeding_draws = []
    abroad_not_direct_proceeding_draws = []
    for draw in proceeding_draws:
        if draw.store.nation == 'Korea':
            if draw.can_delivery == True:
                # print('국내_온라인', draw)
                korea_can_delivery_proceeding_draws.append(draw)
            else:               
                # print('국내_오프라인', draw)
                korea_not_delivery_proceeding_draws.append(draw)
        else:
            if draw.is_direct:
                # print('직배송', draw)
                abroad_direct_proceeding_draws.append(draw)
            else:
                # print('직배송 X', draw)
                abroad_not_direct_proceeding_draws.append(draw)

    # 진행예정
    korea_can_delivery_upcoming_draws = []
    korea_not_delivery_upcoming_draws = []
    abroad_direct_upcoming_draws = []
    abroad_not_direct_upcoming_draws = []
    for draw in upcoming_draws:
        if draw.store.nation == 'Korea':
            if draw.can_delivery == True:
                # print('국내_온라인', draw)
                korea_can_delivery_upcoming_draws.append(draw)
            else:               
                # print('국내_오프라인', draw)
                korea_not_delivery_upcoming_draws.append(draw)
        else:
            if draw.is_direct:
                # print('직배송', draw)
                abroad_direct_upcoming_draws.append(draw)
            else:
                # print('직배송 X', draw)
                abroad_not_direct_upcoming_draws.append(draw)

    # 종료
    korea_can_delivery_finished_draws = []
    korea_not_delivery_finished_draws = []
    abroad_direct_finished_draws = []
    abroad_not_direct_finished_draws = []
    for draw in finished_draws:
        if draw.store.nation == 'Korea':
            if draw.can_delivery == True:
                # print('국내_온라인', draw)
                korea_can_delivery_finished_draws.append(draw)
            else:               
                # print('국내_오프라인', draw)
                korea_not_delivery_finished_draws.append(draw)
        else:
            if draw.is_direct:
                # print('직배송', draw)
                abroad_direct_finished_draws.append(draw)
            else:
                # print('직배송 X', draw)
                abroad_not_direct_finished_draws.append(draw)
    
    # 진행중인 응모개수
    total_proceeding_draw_count = len(proceeding_draws)
    korea_proceeding_draws_count = len(korea_can_delivery_proceeding_draws) + len(korea_not_delivery_proceeding_draws)
    abroad_proceeding_draws_count = len(abroad_direct_proceeding_draws) + len(abroad_not_direct_proceeding_draws)

    context = {
        'product': product,
        'total_proceeding_draw_count': total_proceeding_draw_count,
        'korea_proceeding_draws_count': korea_proceeding_draws_count,
        'abroad_proceeding_draws_count': abroad_proceeding_draws_count,

        'korea_can_delivery_proceeding_draws': korea_can_delivery_proceeding_draws,
        'korea_can_delivery_upcoming_draws': korea_can_delivery_upcoming_draws,
        'korea_can_delivery_finished_draws': korea_can_delivery_finished_draws,
        
        'korea_not_delivery_proceeding_draws': korea_not_delivery_proceeding_draws,
        'korea_not_delivery_upcoming_draws': korea_not_delivery_upcoming_draws,
        'korea_not_delivery_finished_draws': korea_not_delivery_finished_draws,
        
        'abroad_direct_proceeding_draws': abroad_direct_proceeding_draws,
        'abroad_direct_upcoming_draws': abroad_direct_upcoming_draws,
        'abroad_direct_finished_draws': abroad_direct_finished_draws,
        
        'abroad_not_direct_proceeding_draws': abroad_not_direct_proceeding_draws,
        'abroad_not_direct_upcoming_draws': abroad_not_direct_upcoming_draws,
        'abroad_not_direct_finished_draws': abroad_not_direct_finished_draws,       
    }
    return render(request, 'drawa/detail.html', context)


@require_POST
def wish(request, product_pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=product_pk)
        if product.wish.filter(pk=request.user.pk).exists():
            product.wish.remove(request.user)
            wished = False
        else:
            product.wish.add(request.user)
            wished = True 
        
        context = {
            'wished': wished,
            'wish_count':product.wish.count()
        }
        return JsonResponse(context)        
    return HttpResponse(status=401)


@require_POST
def reserve(request, draw_pk):
    if request.user.is_authenticated:
        draw = get_object_or_404(Draw, pk=draw_pk)
        if draw.reserve.filter(pk=request.user.pk).exists():
            draw.reserve.remove(request.user)
            reserved = False
        else:
            draw.reserve.add(request.user)
            reserved = True

        context = {
            'reserved': reserved,
        }

        return JsonResponse(context)
    return HttpResponse(status=401)


@require_POST
def participate(request, draw_pk):
    if request.user.is_authenticated:
        draw = get_object_or_404(Draw, pk=draw_pk)
        if draw.participate.filter(pk=request.user.pk).exists():
            draw.participate.remove(request.user)
            participated = False
        else:
            draw.participate.add(request.user)
            participated = True

        context = {
            'participated': participated,
        }
        return JsonResponse(context)
    return HttpResponse(status=401)


# @login_required
# @require_safe
# def place(request):
#     stores = Store.objects.all()

#     context = {
#         'stores': stores,
#     }
#     return render(request, 'drawa/place.html', context)


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
    if shoes.wish.filter(pk=request.user.pk).exists():
        shoes.wish.remove(request.user)
        interested = False
    # 관심 등록
    else:
        shoes.wish.add(request.user)
        interested = True
    
    # JsonResponse를 통해 응답
    context = {
        'interested': interested,
    }
    return JsonResponse(context)
    
    # 그 전에 있던 페이지로 이동
    # return redirect('drawa:shoes_detail')
    # return redirect('drawa:index')



def favorite(request):
    products = Product.objects.all()
    context = {
        'products': products,        
    }
    return render(request, 'drawa/favorite.html', context)

def info(request):
    # 메인 페이지의 모든 신발 url 획득
    basic_url = 'https://www.shoeprize.com'
    driver = wd.Chrome(executable_path="chromedriver.exe")
    driver.get(basic_url)
    driver.maximize_window()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.select('.img_area a[href]')
    urls = set(urls)
    urls = list(urls)

    second_url = 'https://www.shoeprize.com/drops/'
    driver.get(second_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    urls.extend(soup.select('.calendar_list a[href]'))
    urls = set(urls)
    urls = list(urls)
    print(len(urls))
    # 각 상세 페이지의 신발 정보 획득후 저장
    for i in range(len(urls)):
        url = basic_url + urls[i]['href']
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        image = soup.select('.img_slide_area img[src]')[0]['src']
        brand = soup.select('.brand_info .brand')[0].get_text()
        k_name = soup.select('.brand_info .detail')[0].get_text()
        e_name = soup.select('.brand_info .name')[0].get_text()
        if '컬렉션' in k_name:
            continue
        infos = soup.select('.info_list .text')
        if len(infos) < 4:
            continue
        code = infos[0].get_text()
        temp_price = infos[1].get_text()[1:]
        price = ''
        for char in temp_price:
            if char != ',':
                price += char
        if len(price) < 4:
            price = int(price) * 1180    
        else:
            price = int(price)
        
        temp_date = infos[2].get_text().strip()
        if temp_date == '미정':
            temp_date = '1900-01-01' 
        release_date = datetime.strptime(temp_date, '%Y-%m-%d')
        release_date = tz.make_aware(release_date)

        temp_cnt = soup.select('.detail_info .info .count')[1].get_text()
        view_cnt = ''
        for char in temp_cnt:
            if char != ',':
                view_cnt+= char
        view_cnt = int(view_cnt)
        collection = 'None'
        if 'JORDAN' in e_name:
            collection = e_name[e_name.find('JORDAN'):8]

        if Product.objects.filter(name_kor=k_name).exists() == False:
            Product(
                name_kor=k_name,
                name_eng=e_name,
                brand=brand,
                code = code,
                relesed_date= release_date,
                price = price,
                view_count = view_cnt,
                image_url = image,
                collection = collection,
            ).save()


        all_draw = soup.select('.release_wrap .btn_apply')
        hidden_draw = soup.select('.release_wrap .item_end.hidden')
        height = 100
    
        for j in range(1, len(all_draw) - len(hidden_draw)+1):
            if j > 1:
                driver.execute_script(f"window.scrollTo(0, {height});")
                height += 110
                time.sleep(1)
            driver.find_element_by_xpath(f'//*[@id="productReleaseArea"]/div/ul/li[{j}]/div[2]/div[2]/div/button').click()
            time.sleep(0.5)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            order = soup.select('.lst_detail .tit')
    
            for k in range(len(order)):
                if order[k].get_text().strip() == '응모 기간':
                    temp_date = soup.select('.lst_detail .text')[k].get_text().strip()
                elif order[k].get_text().strip() == '수령 방법':
                    temp_method = soup.select('.lst_detail .text')[k].get_text().strip()
            if '않았습니다' in temp_date:
                start = '2100-01-01 10:10:10'
                end = '2100-01-01 10:10:10'
                start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
                start = tz.make_aware(start)
                end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
                end = tz.make_aware(end)
            elif '~' in temp_date:
                temp_date = temp_date[:37].strip()
                start = '2021-' + temp_date[:temp_date.find('월')].strip() + \
                    '-' + temp_date[temp_date.find('일')-2:temp_date.find('일')].strip() + ' ' + temp_date[temp_date.find(')')+2:temp_date.find(')')+7] \
                     + ':00'
                start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
                start = tz.make_aware(start)

                temp_date = temp_date[temp_date.find('~')+1:]
                end = '2021-' + temp_date[:temp_date.find('월')].strip() + \
                '-' + temp_date[temp_date.find('일')-2:temp_date.find('일')].strip() + ' ' + temp_date[temp_date.find(')')+2:temp_date.find(')')+7] \
                    + ':00'
            elif '마감' in temp_date:
                temp_date = temp_date[:len(temp_date)-3]
                start = datetime.now()
                end = '2021-' + temp_date[:temp_date.find('월')].strip() + \
                '-' + temp_date[temp_date.find('일')-2:temp_date.find('일')].strip() + ' ' + temp_date[temp_date.find(')')+2:temp_date.find(')')+7] \
                    + ':00'
                end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
                end = tz.make_aware(end)
            elif '시작' in temp_date:
                temp_date = temp_date[:temp_date.find('시작')-1]
                end = '2100-01-01 10:10:10'
                start = '2021-' + temp_date[:temp_date.find('월')].strip() + \
                    '-' + temp_date[temp_date.find('일')-2:temp_date.find('일')].strip() + ' ' + temp_date[temp_date.find(')')+2:temp_date.find(')')+7] \
                     + ':00'

                start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
                start = tz.make_aware(start)
                end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
                end = tz.make_aware(end)
            
            if len(soup.select('.btn_draw')) != 0:
                url = soup.select('.btn_draw')[0]['data-url']
            elif len(soup.select('.btn_done')) != 0:
                url = soup.select('.btn_done')[0]['data-url']
            elif len(soup.select('.btn_release')) != 0:
                url = soup.select('.btn_release')[0]['data-url']
           
            if temp_method == '배대지':
                delivery = False
                direct = False
            elif temp_method == '직배':
                delivery = False
                direct = True
            elif temp_method == '매장 수령':
                delivery = True
                direct = False
            elif temp_method == '국내 배송':
                delivery = True
                direct = True

            store = soup.select('.popup_content .brand_info .info_area .name')[0].get_text()
            store_img = soup.select('.popup_content .brand_info img[src]')[0]['src']
            if Store.objects.filter(name=store).exists() == False:
                Store(
                    name = store,
                    store_img_url = store_img,
                ).save()
        
            pro = Product.objects.get(name_kor = k_name)
            st = Store.objects.get(name = store)
            Draw(
                can_delivery = delivery,
                product = pro,
                store = st,
                url = url,
                start = start,
                end = end,
                is_direct = direct,
            ).save()
            driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/button[2]').click() # X버튼
    return redirect('drawa:index')


def mail(request, draw_pk):
    draw = get_object_or_404(Draw, pk=draw_pk)

    email = request.user.email
    if email is not None:
        subject = f'[드로와] { request.user.first_name }님의 드로우가 시작되었습니다!'
        message = f'''
            { request.user.first_name }님의 드로우가 시작되었습니다!

            👟 드로우 정보
            제품 : {draw.product.name_kor}
            응모 바로가기 ▶ {draw.url}
        '''
        mail = EmailMessage(subject, message, to=[email])
        mail.send()
    
    return redirect('drawa:index')