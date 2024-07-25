import os
import django
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

from api.models import Restaurant, Menu

# Sample menu data
menu_data = [
    {
        "name": "Nepali Menu",
        "items": [
            {"name": "Dal Bhat", "price": 338, "category": "Food"},
            {"name": "Momo", "price": 169, "category": "Food"},
            {"name": "Newari Khaja Set", "price": 676, "category": "Lunch"},
            {"name": "Aloo Tama", "price": 253, "category": "Dinner"},
            {"name": "Sel Roti", "price": 84, "category": "Beverages"}
        ]
    },
    {
        "name": "Newari Menu",
        "items": [
            {"name": "Yomari", "price": 253, "category": "Food"},
            {"name": "Chatamari", "price": 253, "category": "Food"},
            {"name": "Chhoyela", "price": 423, "category": "Lunch"},
            {"name": "Bara", "price": 169, "category": "Dinner"},
            {"name": "Sapu Mhicha", "price": 423, "category": "Beverages"}
        ]
    },
    {
        "name": "Indian Menu",
        "items": [
            {"name": "Butter Chicken", "price": 845, "category": "Food"},
            {"name": "Paneer Tikka", "price": 507, "category": "Food"},
            {"name": "Masala Dosa", "price": 338, "category": "Lunch"},
            {"name": "Biryani", "price": 591, "category": "Dinner"},
            {"name": "Naan", "price": 84, "category": "Beverages"}
        ]
    },
    {
        "name": "Thai Menu",
        "items": [
            {"name": "Pad Thai", "price": 591, "category": "Food"},
            {"name": "Green Curry", "price": 591, "category": "Food"},
            {"name": "Tom Yum Soup", "price": 423, "category": "Lunch"},
            {"name": "Thai Spring Rolls", "price": 253, "category": "Dinner"},
            {"name": "Sticky Rice with Mango", "price": 338, "category": "Beverages"}
        ]
    },
    {
        "name": "Italian Menu",
        "items": [
            {"name": "Margherita Pizza", "price": 507, "category": "Food"},
            {"name": "Spaghetti Carbonara", "price": 591, "category": "Food"},
            {"name": "Lasagna", "price": 591, "category": "Lunch"},
            {"name": "Bruschetta", "price": 253, "category": "Dinner"},
            {"name": "Tiramisu", "price": 338, "category": "Beverages"}
        ]
    },
    {
        "name": "Fast Food Menu",
        "items": [
            {"name": "Cheeseburger", "price": 253, "category": "Food"},
            {"name": "French Fries", "price": 169, "category": "Food"},
            {"name": "Hot Dog", "price": 169, "category": "Lunch"},
            {"name": "Chicken Nuggets", "price": 253, "category": "Dinner"},
            {"name": "Milkshake", "price": 253, "category": "Beverages"}
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

        # Create Menu items for the selected items
        for item in selected_items:
            Menu.objects.create(
                restaurant=restaurant,
                name=item["name"],
                price=item["price"],
                category=item["category"]
            )

        print(f'Successfully assigned menu items to restaurant {restaurant.name}')

if __name__ == "__main__":
    assign_menu_items()
