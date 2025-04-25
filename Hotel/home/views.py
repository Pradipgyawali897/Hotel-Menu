from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Item, Topic
from .forms import ItemForm

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('list_items')
        else:
            try:
                User.objects.get(username=username)
                messages.error(request, 'Invalid password.')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
    context = {}
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('loginpage')

@login_required(login_url='loginpage')
def list_items(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    items = Item.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
    )
    items_count = items.count()
    topics = Topic.objects.all()
    return render(request, 'index.html', {'items': items, 'topics': topics, 'items_count': items_count})

@login_required(login_url='loginpage')
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.host = request.user  # Set the host
            item.save()
            messages.success(request, 'Item added successfully!')
            return redirect('list_items')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})

@login_required(login_url='loginpage')
def view_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    messages.success(request, 'Item viewed successfully!')
    return render(request, 'index.html', {'items': [item], 'topics': Topic.objects.all()})

@login_required(login_url='loginpage')
def update_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.user != item.host:
        messages.error(request, 'You are not authorized to update this item.')
        return redirect('list_items')
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('list_items')
        else:
            messages.error(request, 'Failed to update item. Please check the form.')
    else:
        form = ItemForm(instance=item)
    return render(request, 'update_item.html', {'form': form})

@login_required(login_url='loginpage')
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.user != item.host:
        messages.error(request, 'You are not authorized to delete this item.')
        return redirect('list_items')
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('list_items')
    return render(request, 'delete.html', {'obj': item})