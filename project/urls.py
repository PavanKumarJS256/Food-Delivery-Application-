"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

from app.views import add_favorite, add_food, add_restaurant, admin_rest_list, adminhome, edit_profile, order_food, order_food_done, profile, register, restaurant_foods, restaurant_list, restdelete, restupdate, submit_review, user_login, userhome, validatedelete, validateupdate, view_favorites

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin_rest_list/',admin_rest_list,name='admin_rest_list'),
    path('restaurants/', restaurant_list, name='restaurant_list'),
    path('restaurants_foods/<int:restaurant_id>/', restaurant_foods, name='restaurant_foods'),
    path('restaurants/add/',add_restaurant, name='add_restaurant'),
    path('foods/add/',add_food, name='add_food'),
    path('adminhome/',adminhome),
    path('userhome/',userhome,name='userhome'),
    path('restdelete/',restdelete),
    path('validatedelete/',validatedelete,name='validatedelete'),
    path('restupdate/',restupdate),
    path('validateupdate/',validateupdate,name='validateupdate'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('order/<int:food_id>/', order_food, name='order_food'),
    path('order_food_done/',order_food_done,name='order_food_done'),
    path('submit_review/<str:order_id>/',submit_review, name='submit_review'),
    path('edit_profile/', edit_profile, name='edit_profile'),

    #path('add_favorite/<int:restaurant_id>/',add_favorite, name='add_favorite'),
    #path('favorites/',view_favorites, name='favorites'),
]



