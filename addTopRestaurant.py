
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

from api.models import Restaurant, TopRestaurant


# Define the restaurant IDs and their corresponding rankings
restaurant_ids = [2, 4, 6]
rankings = [1, 2, 3]

if __name__ == "__main__":
    # Iterate over the restaurant IDs and rankings to create TopRestaurant instances
    for restaurant_id, ranking in zip(restaurant_ids, rankings):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            TopRestaurant.objects.create(restaurant=restaurant, ranking=ranking)
            print(f"Added Restaurant ID {restaurant_id} as TopRestaurant with ranking {ranking}")
        except Restaurant.DoesNotExist:
            print(f"Restaurant with ID {restaurant_id} does not exist.")
