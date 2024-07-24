import os
import django
import random

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

from api.models import Tag, Restaurant

# Define your tags
TAGS = [
    'Italian', 'Chinese', 'Indian', 'Mexican', 'Thai', 'Japanese', 
    'American', 'French', 'Mediterranean', 'Vegetarian', 'Vegan', 
    'Gluten-Free', 'Nepali', 'Newari', 'Korean', 'Vietnamese', 'Greek', 
    'Middle Eastern', 'Seafood', 'Barbecue', 'Pizza', 'Burger', 
    'Fast Food', 'Dessert', 'Bakery', 'Cafe', 'Flavorful', 'Kid Friendly', 
    'Vegan Options', 'Live Music', 'Pet Friendly', 'Parking', 
    'Ambience', 'Delivery Service', 'Outdoor Seating', 'Family-Friendly', 
    'Peaceful', 'Accommodation', 'Breakfast', 'Lunch', 'Dinner', 'Bar', 
    'Private Space', 'Organic', 'Couple Friendly'
]

def create_tags():
    # Create the tags if they do not exist
    for tag_name in TAGS:
        Tag.objects.get_or_create(name=tag_name)

def assign_tags_to_restaurants():
    # Get the restaurants with IDs from 1 to 9
    restaurants = Restaurant.objects.filter(id__in=range(1, 10))
    tags = list(Tag.objects.all())
    
    # Assign a random number of random tags to each restaurant
    for restaurant in restaurants:
        random_tags = random.sample(tags, k=random.randint(1, len(tags) // 2))
        restaurant.tags.set(random_tags)
        restaurant.save()

if __name__ == '__main__':
    create_tags()
    assign_tags_to_restaurants()
    print('Random tags assigned to restaurants.')
