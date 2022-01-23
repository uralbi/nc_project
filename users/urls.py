from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('post/', login_required(PostProduct.as_view()), name='post_product' ),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete'),
    path('products/<int:pk>/', ViewProduct.as_view(), name='view_product'),
]