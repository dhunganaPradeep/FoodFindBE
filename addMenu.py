import os
import django
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

from api.models import Restaurant, MenuItem

# Sample menu data
menu_data = [
    {
        "name": "Nepali Menu",
        "items": [
            {"name": "Dal Bhat", "price": 338},
            {"name": "Momo", "price": 169},
            {"name": "Newari Khaja Set", "price": 676},
            {"name": "Aloo Tama", "price": 253},
            {"name": "Sel Roti", "price": 84}
        ]
    },
    {
        "name": "Newari Menu",
        "items": [
            {"name": "Yomari", "price": 253},
            {"name": "Chatamari", "price": 253},
            {"name": "Chhoyela", "price": 423},
            {"name": "Bara", "price": 169},
            {"name": "Sapu Mhicha", "price": 423}
        ]
    },
    {
        "name": "Indian Menu",
        "items": [
            {"name": "Butter Chicken", "price": 845},
            {"name": "Paneer Tikka", "price": 507},
            {"name": "Masala Dosa", "price": 338},
            {"name": "Biryani", "price": 591},
            {"name": "Naan", "price": 84}
        ]
    },
    {
        "name": "Thai Menu",
        "items": [
            {"name": "Pad Thai", "price": 591},
            {"name": "Green Curry", "price": 591},
            {"name": "Tom Yum Soup", "price": 423},
            {"name": "Thai Spring Rolls", "price": 253},
            {"name": "Sticky Rice with Mango", "price": 338}
        ]
    },
    {
        "name": "Italian Menu",
        "items": [
            {"name": "Margherita Pizza", "price": 507},
            {"name": "Spaghetti Carbonara", "price": 591},
            {"name": "Lasagna", "price": 591},
            {"name": "Bruschetta", "price": 253},
            {"name": "Tiramisu", "price": 338}
        ]
    },
    {
        "name": "Fast Food Menu",
        "items": [
            {"name": "Cheeseburger", "price": 253},
            {"name": "French Fries", "price": 169},
            {"name": "Hot Dog", "price": 169},
            {"name": "Chicken Nuggets", "price": 253},
            {"name": "Milkshake", "price": 253}
        ]
    }
]

def assign_menu_items():
    # Get all restaurants with IDs 1 to 9
    restaurants = Restaurant.objects.filter(id__in=range(1, 10))

    for restaurant in restaurants:
        # Select 12-20 random items from the menu data
        restaurant.menu_items.all().delete()
        selected_items = []
        while len(selected_items) < 18:
            menu = random.choice(menu_data)
            item = random.choice(menu["items"])
            if item not in selected_items:
                selected_items.append(item)

        # Create MenuItems for the selected items
        for item in selected_items:
            # Format the price with ".00"
            formatted_price = f'{item["price"]}.00'
            MenuItem.objects.create(
                restaurant=restaurant,
                name=item["name"],
                price=formatted_price
            )

        print(f'Successfully assigned menu items to restaurant {restaurant.name}')

if __name__ == "__main__":
    assign_menu_items()