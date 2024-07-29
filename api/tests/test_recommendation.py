from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import CustomUser, Restaurant, Review, Tag

class RecommendationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users with unique email addresses and google_ids
        self.user1 = CustomUser.objects.create_user(username='user1', email='user1@example.com', password='password', google_id='user1_google_id')
        self.user2 = CustomUser.objects.create_user(username='user2', email='user2@example.com', password='password', google_id='user2_google_id')

        # Create tags
        self.tag1 = Tag.objects.create(name='Italian')
        self.tag2 = Tag.objects.create(name='Chinese')

        # Create restaurants
        self.restaurant1 = Restaurant.objects.create(name='Restaurant 1', location='Location 1', price='$$', opening_hours='9am-9pm', description='Desc 1')
        self.restaurant2 = Restaurant.objects.create(name='Restaurant 2', location='Location 2', price='$$', opening_hours='9am-9pm', description='Desc 2')

        # Assign tags
        self.restaurant1.tags.add(self.tag1)
        self.restaurant2.tags.add(self.tag2)

        # Create reviews and favorites
        Review.objects.create(user=self.user1, restaurant=self.restaurant1, rating=5, review_text='Great!')
        self.user1.favorite_restaurants.add(self.restaurant1)

    def test_recommendations(self):
        # Authenticate user1
        self.client.login(username='user1', password='password')

        # Get recommendations for user1
        response = self.client.get('/restaurants/', {'recommend': 'true'})
        
        # Debugging information
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the recommendations
        recommended_restaurants = response.json()
        print("Recommended restaurants:", recommended_restaurants)
        self.assertTrue(any(r['id'] == self.restaurant2.id for r in recommended_restaurants), "Restaurant 2 should be in recommendations")

        # Clean up login session
        self.client.logout()



    # def test_no_recommendations_for_anonymous(self):
    #     # Get recommendations for anonymous user
    #     response = self.client.get('/api/restaurants/', {'recommend': 'true'})
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
