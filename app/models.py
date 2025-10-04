from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Restaurant(models.Model):
    rest_id=models.CharField(max_length=100)
    rest_name = models.CharField(max_length=100)
    rest_type = models.CharField(max_length=255)
    
    # Add other fields as necessary

    def __str__(self):
        return self.rest_name

class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    des=models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='foods')
    
    # Add other fields as necessary

    def __str__(self):
        return self.name
    

class Restaurants(models.Model):
    rest_id=models.CharField(max_length=100)
    rest_name= models.CharField(max_length=100)
    rest_type= models.CharField(max_length=255)
    rest_img=models.CharField(max_length=255)
    # Add other fields as necessary

    def __str__(self):
        return self.rest_name

class Foods(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    des=models.CharField(max_length=100)
    food_img=models.CharField(max_length=255)
    restaurant= models.ForeignKey(Restaurants, on_delete=models.CASCADE, related_name='foods')

    # Add other fields as necessary

    def __str__(self):
        return self.name
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Foods, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=100, unique=True)  # Add this field


    def __str__(self):
        return f'Order by {self.user.username} for {self.food.name}'



class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for Order {self.order.order_id} by {self.user.username}'
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.restaurant.rest_name}'

