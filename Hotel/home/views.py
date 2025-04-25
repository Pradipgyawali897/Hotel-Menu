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
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('list_items')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Validate required fields
        if not username or not password:
            messages.error(request, 'Both username and password are required.')
            return render(request, 'login.html')
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            
            # Redirect to the page user was trying to access if specified in next parameter
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('list_items')
        else:
            try:
                User.objects.get(username=username)
                messages.error(request, 'Invalid password. Please try again.')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist. Please check the username.')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('loginpage')

def list_items(request):
    q = request.GET.get('q', '')
    
    # Search functionality
    if q:
        items = Item.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
    else:
        items = Item.objects.all()
        
    items_count = items.count()
    topics = Topic.objects.all().order_by('name')
    
    context = {
        'items': items,
        'topics': topics,
        'items_count': items_count,
        'search_query': q
    }
    return render(request, 'index.html', context)

@login_required(login_url='loginpage')
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.host = request.user
            item.save()
            messages.success(request, f'Item "{item.name}" added successfully!')
            return redirect('list_items')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ItemForm()
    
    return render(request, 'add_item.html', {'form': form})

@login_required(login_url='loginpage')
def view_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'view_item.html', {'item': item})

@login_required(login_url='loginpage')
def update_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    
    # Check if user is authorized
    if request.user != item.host:
        messages.error(request, 'You are not authorized to update this item.')
        return redirect('list_items')
        
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Item "{item.name}" updated successfully!')
            return redirect('list_items')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'update_item.html', {'form': form})

@login_required(login_url='loginpage')
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    # Check if user is authorized
    if request.user != item.host:
        messages.error(request, 'You are not authorized to delete this item.')
        return redirect('list_items')
        
    if request.method == 'POST':
        item_name = item.name
        item.delete()
        messages.success(request, f'Item "{item_name}" deleted successfully!')
        return redirect('list_items')
    
    return render(request, 'delete.html', {'obj': item})