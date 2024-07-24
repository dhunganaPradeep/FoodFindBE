import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()
import random
from django.utils import timezone
from api.models import Restaurant, Review, CustomUser

# Set up Django environment

# Create some users
user_data = [
    {'username': 'john_doe', 'email': 'john_doe@example.com', 'google_id': 'google_1'},
    {'username': 'jane_smith', 'email': 'jane_smith@example.com', 'google_id': 'google_2'},
    {'username': 'alice_jones', 'email': 'alice_jones@example.com', 'google_id': 'google_3'},
    {'username': 'michael_brown', 'email': 'michael_brown@example.com', 'google_id': 'google_4'},
    {'username': 'linda_white', 'email': 'linda_white@example.com', 'google_id': 'google_5'},
    {'username': 'robert_jackson', 'email': 'robert_jackson@example.com', 'google_id': 'google_6'},
    {'username': 'patricia_clark', 'email': 'patricia_clark@example.com', 'google_id': 'google_7'},
    {'username': 'mary_lee', 'email': 'mary_lee@example.com', 'google_id': 'google_8'},
    {'username': 'james_wilson', 'email': 'james_wilson@example.com', 'google_id': 'google_9'},
    {'username': 'barbara_moore', 'email': 'barbara_moore@example.com', 'google_id': 'google_10'},
]

users = []
for data in user_data:
    user, created = CustomUser.objects.get_or_create(
        username=data['username'], 
        defaults={
            'email': data['email'],
            'google_id': data['google_id']
        }
    )
    if created:
        user.set_password('password123')
        user.save()
    users.append(user)

# Realistic review texts
review_texts = [
    "The food was absolutely wonderful, from preparation to presentation, very pleasing.",
    "My experience here was amazing! The ambiance was perfect and the food was delicious.",
    "Great place to eat! The service was exceptional and the menu had a variety of options.",
    "I really enjoyed my meal here. The staff were friendly and the environment was cozy.",
    "This restaurant exceeded my expectations! The dishes were flavorful and well-prepared.",
    "Fantastic experience! The portions were generous and the prices were reasonable.",
    "Loved the food here! The ingredients were fresh and the flavors were spot on.",
    "A delightful dining experience. The staff was attentive and the food was top-notch.",
    "Highly recommend this place. The food was great and the atmosphere was welcoming.",
    "A hidden gem! The service was prompt and the food was exquisite."
]

# Function to create realistic reviews
def create_review(user, restaurant, review_text):
    rating = random.choice([3, 4, 5])
    Review.objects.create(
        user=user,
        restaurant=restaurant,
        rating=rating,
        review_text=review_text,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )

# Restaurant IDs to create reviews for
restaurant_ids = [1, 2, 4, 6, 8, 9]

# Create reviews for the specified restaurants
for restaurant_id in restaurant_ids:
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        for user in users:
            review_text = random.choice(review_texts)
            create_review(user, restaurant, review_text)
            print(f"Created review for Restaurant ID {restaurant_id} by {user.username}")
    except Restaurant.DoesNotExist:
        print(f"Restaurant with ID {restaurant_id} does not exist.")
