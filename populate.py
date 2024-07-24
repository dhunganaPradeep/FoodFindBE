# populate_database.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

import json
from api.models import Restaurant, RestaurantImage

def populate_database():
    with open('restaurants_data.json', 'r') as file:
        data = json.load(file)
        for restaurant_data in data:
            images_exist = all(os.path.exists(image_path) for image_path in restaurant_data['images'])
            if images_exist:
                restaurant = Restaurant.objects.create(
                    name=restaurant_data['name'],
                    location=restaurant_data['location'],
                    price=restaurant_data['price'],
                    opening_hours=restaurant_data['opening_hours'],
                    description=restaurant_data['description']
                )
                for i in range(5):
                        try:
                            with open(restaurant_data['images'][i], 'rb') as img_file:
                                image = RestaurantImage(restaurant=restaurant)
                                image.image.save(os.path.basename(restaurant_data['images'][i]), img_file)
                        except OSError as e:
                            print(f"Error opening file '{restaurant_data['images'][i]}': {e}")
            else:
                print(f"Skipping restaurant '{restaurant_data['name']}' because images do not exist.")

if __name__ == '__main__':
    populate_database()
