from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item, RentalRequest
from .forms import ItemForm, RentalRequestForm
from datetime import date, timedelta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import ItemForm

def home(request):
    # 내가 등록한 물품
    my_items = []
    if request.user.is_authenticated:
        my_items = Item.objects.filter(owner=request.user)

        # 대여 상태를 계산하여 추가
        my_items_with_status = []
        for item in my_items:
            is_rented = item.rental_requests.filter(status='Approved').exists()
            my_items_with_status.append({
                'item': item,
                'is_rented': is_rented
            })
    else:
        my_items_with_status = []

    # 대여 가능한 물품 (로그인하지 않았거나 본인이 등록하지 않은 물품)
    available_items = Item.objects.filter(is_available=True)
    if request.user.is_authenticated:
        available_items = available_items.exclude(owner=request.user).exclude(rental_requests__status='Approved')

    return render(request, 'rentals/home.html', {
        'my_items_with_status': my_items_with_status,
        'available_items': available_items
    })



def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    approved_rentals = RentalRequest.objects.filter(item=item, status='Approved')
    return render(request, 'rentals/item_detail.html', {
        'item': item,
        'approved_rentals': approved_rentals
    })

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'rentals/add_item.html', {'form': form})

@login_required
def request_rental(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = RentalRequestForm(request.POST)
        if form.is_valid():
            rental_request = form.save(commit=False)
            rental_request.requester = request.user
            rental_request.item = item
            rental_request.save()
            return redirect('home')
    else:
        form = RentalRequestForm()
    return render(request, 'rentals/request_rental.html', {'form': form, 'item': item})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'rentals/signup.html', {'form': form})


@login_required
def my_items(request):
    # 사용자가 등록한 상품
    items = Item.objects.filter(owner=request.user)
    
    # 요청이 승인된 상품
    approved_items = items.filter(rental_requests__status='Approved').distinct()
    
    # 등록 중인 상품 (승인된 요청이 없는 상품)
    available_items = items.exclude(id__in=approved_items)

    return render(request, 'rentals/my_items.html', {
        'approved_items': approved_items,
        'available_items': available_items
    })

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('my_items')
    return render(request, 'rentals/delete_item.html', {'item': item})
from django.shortcuts import redirect

@login_required
def manage_requests(request):
    # 상태가 Pending인 요청만 필터링
    rental_requests = RentalRequest.objects.filter(item__owner=request.user, status='Pending')
    return render(request, 'rentals/manage_requests.html', {'rental_requests': rental_requests})


@login_required
def approve_request(request, pk):
    rental_request = get_object_or_404(RentalRequest, pk=pk, item__owner=request.user)
    rental_request.status = 'Approved'

    # 대여 기간 설정 (예시: 대여 시작일은 오늘, 종료일은 7일 후)
    from datetime import date, timedelta
    rental_request.start_date = date.today()
    rental_request.end_date = date.today() + timedelta(days=7)

    rental_request.save()
    return redirect('manage_requests')


@login_required
def reject_request(request, pk):
    rental_request = get_object_or_404(RentalRequest, pk=pk, item__owner=request.user)
    rental_request.status = 'Rejected'
    rental_request.save()
    return redirect('manage_requests')




@login_required
def approve_request(request, pk):
    rental_request = get_object_or_404(RentalRequest, pk=pk, item__owner=request.user)
    rental_request.status = 'Approved'
    rental_request.save()

    # 아이템을 대여 불가 상태로 업데이트
    rental_request.item.is_available = False
    rental_request.item.save()

    return redirect('manage_requests')




@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('my_items')
    else:
        form = ItemForm(instance=item)
    return render(request, 'rentals/edit_item.html', {'form': form, 'item': item})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import RentalRequest

@login_required
def my_rented_items(request):
    # 현재 사용자가 대여 중인 물품
    rented_items = RentalRequest.objects.filter(
        requester=request.user, status='Approved'
    ).select_related('item')
    return render(request, 'rentals/my_rented_items.html', {'rented_items': rented_items})
