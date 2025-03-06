from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ShoppingItem

# Create your views here.

@login_required
def shopping_list(request):
    active_items = ShoppingItem.objects.filter(purchased=False)
    purchased_items = ShoppingItem.objects.filter(purchased=True)[:10]  # Show last 10 purchased items
    return render(request, 'shopping/list.html', {
        'active_items': active_items,
        'purchased_items': purchased_items
    })

@login_required
def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            ShoppingItem.objects.create(
                name=name,
                created_by=request.user
            )
            messages.success(request, 'Item added successfully!')
        return redirect('shopping:list')

@login_required
def toggle_purchased(request, item_id):
    try:
        item = ShoppingItem.objects.get(id=item_id)
        item.purchased = not item.purchased
        item.save()
        messages.success(request, 'Item updated successfully!')
    except ShoppingItem.DoesNotExist:
        messages.error(request, 'Item not found!')
    return redirect('shopping:list')
