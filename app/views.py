import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, UserRegistrationForm
from .models import Review
from .forms import ReviewForm
from .models import Favorite, Restaurant
from .forms import EditProfileForm


# Create your views here.
from django.shortcuts import render, get_object_or_404

from app.forms import FoodForm, RestaurantForm
from .models import Order, Restaurants, Foods

def restaurant_list(request):
    restaurants = Restaurants.objects.all()
    return render(request, 'restaurant_list.html', {'restaurants': restaurants})

def restaurant_foods(request, restaurant_id):
    restaurant = get_object_or_404(Restaurants, id=restaurant_id)
    foods = restaurant.foods.all()
    return render(request, 'restaurant_foods.html', {'restaurant': restaurant, 'foods': foods})

def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_rest_list')
    else:
        form = RestaurantForm()
    return render(request, 'add_restaurant.html', {'form': form})

def add_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_rest_list')  # Change to appropriate redirect
    else:
        form = FoodForm()
    return render(request, 'add_food.html', {'form': form})

def adminhome(request):
    return render(request,'adminhome.html')

def userhome(request):
    return render(request,'userhome.html')

def admin_rest_list(request):
    rest=Restaurants.objects.all()
    return render(request,'admin_rest_list.html',{'rest':rest})

def restdelete(request):
    return render(request,'delete_rest.html')

def validatedelete(request):
    if request.method=='POST':
        res_id=request.POST.get("id")
        res=Restaurants.objects.filter(rest_id=res_id).first()
        if res:
            res.delete()
            return render(request,'deletego.html')
        else:
            return render(request,'deletego.html')
    else:
        return HttpResponse("Invalid Response")
    
def restupdate(request):
    return render(request,'update_rest.html')


def validateupdate(request):
    if request.method == 'POST':
        res_id = request.POST.get("id")
        new_name = request.POST.get("new_name")
        new_des = request.POST.get("new_des")

        # Find the restaurant by res_id
        res = Restaurants.objects.filter(rest_id=res_id).first()
        
        if res:
            # Update the restaurant details
            res.rest_name = new_name
            res.rest_type = new_des
            
            res.save()
            return render(request,'updatego.html')
        else:
            return HttpResponse("Restaurant not found")
    else:
        return HttpResponse("Invalid request method")
    

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('userhome')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def profile(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'profile.html', {'orders': orders})


def order_food(request, food_id):
    food = get_object_or_404(Foods, id=food_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.food = food
            order.order_id = str(uuid.uuid4())
            order.save()
            
            subject = 'Order Confirmation'
            message = f"Thank you for your order!\n\nOrder ID: {order.order_id}\nFood: {food.name}\nRestaurant: {food.restaurant.rest_name}\nPrice: ${food.price}\n\nYour order will be delivered to:\n{order.address}"
            recipient_list = [request.user.email]
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
            
            return redirect('order_food_done')  # Redirect to a success page or home
    else:
        form = OrderForm()
    return render(request, 'order_food.html', {'form': form, 'food': food})

def order_food_done(request):
    return render(request,'order_food_done.html')



@login_required
def submit_review(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.user = request.user
            review.save()
            return redirect('profile')  # Redirect to profile or another appropriate page
    else:
        form = ReviewForm()

    return render(request, 'submit_review.html', {'form': form, 'order': order})


@login_required
def add_favorite(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
    return redirect('restaurant_list')  

@login_required
def view_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'view_favorites.html', {'favorites': favorites})


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})
