from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_items, name='list_items'),
    path('add/', views.add_item, name='add_item'),
    path('view/<int:item_id>/', views.view_item, name='view_item'),
    path('update/<int:item_id>/', views.update_item, name='update_item'),
    path('delete/<int:pk>/', views.delete_item, name='delete_item'),
    path('login/', views.loginpage, name='loginpage'),
    path('logout/', views.logout_view, name='logout'),
]