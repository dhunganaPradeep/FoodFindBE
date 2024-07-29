from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import CustomUser, Restaurant, Review, Tag

class RecommendationTests(TestCase):
    def setUp(self):
        # Ensure unique google_id for each user
        self.user1 = CustomUser.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password',
            google_id='unique_google_id_1'
        )
        self.user2 = CustomUser.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password',
            google_id='unique_google_id_2'
        )
        
        self.restaurant1 = Restaurant.objects.create(name='Restaurant 1', location='Location 1')
        self.restaurant2 = Restaurant.objects.create(name='Restaurant 2', location='Location 2')
        
        self.tag1 = Tag.objects.create(name='Italian')
        self.tag2 = Tag.objects.create(name='Mexican')

        self.restaurant1.tags.add(self.tag1)
        self.restaurant2.tags.add(self.tag1, self.tag2)

        self.user1.favorite_restaurants.add(self.restaurant1)
        self.user2.favorite_restaurants.add(self.restaurant2)

        Review.objects.create(user=self.user1, restaurant=self.restaurant1, rating=5)
        Review.objects.create(user=self.user2, restaurant=self.restaurant2, rating=4)


    def test_recommendations(self):
        response = self.client.get('/api/restaurants/', {'recommend': 'true', 'user_id': self.user1.id})
        self.assertEqual(response.status_code, 200)
        recommended_restaurants = response.json()
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        print(f"Recommended restaurants: {recommended_restaurants}")
        self.assertTrue(any(r['id'] == self.restaurant2.id for r in recommended_restaurants), "Restaurant 2 should be in recommendations")

