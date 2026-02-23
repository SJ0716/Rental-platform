from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='rentals/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('item/add/', views.add_item, name='add_item'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('request/<int:item_id>/', views.request_rental, name='request_rental'),
    path('my-items/', views.my_items, name='my_items'),
    path('delete-item/<int:pk>/', views.delete_item, name='delete_item'),
    path('manage-requests/', views.manage_requests, name='manage_requests'),
    path('approve-request/<int:pk>/', views.approve_request, name='approve_request'),
    path('reject-request/<int:pk>/', views.reject_request, name='reject_request'),
    path('edit-item/<int:pk>/', views.edit_item, name='edit_item'),
    path('my-rented-items/', views.my_rented_items, name='my_rented_items'),
]
