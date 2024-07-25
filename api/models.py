
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models import Avg

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    opening_hours = models.CharField(max_length=100)
    description = models.TextField()
    map_url = models.CharField(max_length=500,default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7273.904211293504!2d85.307945566468!3d27.67357411547265!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39eb192d79c4bca5%3A0xa7f535ecc88e78d8!2sCHi-CHi!5e0!3m2!1sen!2snp!4v1717407139008!5m2!1sen!2snp")
    tags = models.ManyToManyField(Tag, related_name='restaurants')
    def average_rating(self):
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        return round(avg_rating)

    def __str__(self):
        return self.name
    
    def no_of_reviews(self):
        return self.reviews.count()


class CustomUser(AbstractUser):
    google_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    profile_picture = models.URLField(null=True,default=None)
    favorite_restaurants = models.ManyToManyField(Restaurant, related_name='favorited_by')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        related_query_name='custom_user',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        related_query_name='custom_user',
        blank=True,
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username
    

class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_images/')

from django.db import models
from api.models import Restaurant, RestaurantImage

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menu_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=[
        ('Food', 'Food'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Beverages', 'Beverages'),
        # Add more categories as needed
    ])

    def __str__(self):
        return f"{self.name} - ${self.price}"

    def get_category_display(self):
        return dict(Menu._meta.get_field('category').choices)[self.category]


class Review(models.Model):
    user = models.ForeignKey(CustomUser, related_name='reviews', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rating: {self.rating} for {self.restaurant.name}"

class TopRestaurant(models.Model):
    restaurant = models.OneToOneField('Restaurant', on_delete=models.CASCADE, related_name='top_restaurant')
    ranking = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.restaurant.name} - Ranking: {self.ranking}"


class AddRestaurant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='add_requests')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    opening_hours = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    menu = models.ImageField(upload_to='RequestedMenus/', blank=True, null=True)
