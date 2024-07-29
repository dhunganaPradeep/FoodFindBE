from rest_framework import viewsets
from .models import Restaurant
from .models import TopRestaurant
from rest_framework import generics 
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Tag
from django.db.models import Count, Q, Avg
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta



from .serializers import TopRestaurantSerializer
from .serializers import RestaurantListSerializer
from .serializers import RestaurantDetailSerializer
from .serializers import TagSerializer
from .serializers import CreateReviewSerializer
from .serializers import ReviewSerializer
from .serializers import FavoriteRestaurantSerializer
from .serializers import AddRestaurantSerializer
from .serializers import MenuImageSerializer
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser
from .models import Review
from .models import AddRestaurant
from .models import MenuImage
from .serializers import CustomUserSerializer
import requests

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RestaurantDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        recommend = self.request.query_params.get('recommend') == 'true'
        tags = self.request.query_params.getlist('tags')

        if recommend:
            if user_id:
                user = get_object_or_404(CustomUser, id=user_id)
                queryset = self.get_recommended_restaurants(user)
            else:
                raise NotFound(detail="User ID is required for recommendations")
        elif tags:
            queryset = queryset.annotate(
                matching_tags_count=Count(
                    'tags', filter=Q(tags__name__in=tags))
            ).order_by('-matching_tags_count', 'id')

        return queryset

    def get_recommended_restaurants(self, user):
        # Debugging
        print(f"User: {user}")
        
        user_favorites = user.favorite_restaurants.all()
        print(f"User Favorites: {user_favorites}")
        
        user_reviews = Review.objects.filter(user=user)
        print(f"User Reviews: {user_reviews}")

        similar_users = CustomUser.objects.filter(
            Q(favorite_restaurants__in=user_favorites) |
            Q(reviews__restaurant__in=[review.restaurant for review in user_reviews])
        ).exclude(id=user.id).distinct()
        print(f"Similar Users: {similar_users}")

        collaborative_recommendations = Restaurant.objects.filter(
            Q(favorited_by__in=similar_users) |
            Q(reviews__user__in=similar_users)
        ).exclude(
            Q(favorited_by=user) |
            Q(reviews__user=user)
        ).distinct()
        print(f"Collaborative Recommendations: {collaborative_recommendations}")

        user_tags = Tag.objects.filter(restaurants__in=user_favorites).distinct()
        print(f"User Tags: {user_tags}")

        content_recommendations = Restaurant.objects.filter(tags__in=user_tags).exclude(
            Q(favorited_by=user) |
            Q(reviews__user=user)
        ).distinct()
        print(f"Content Recommendations: {content_recommendations}")

        recommended_restaurants = (collaborative_recommendations | content_recommendations).distinct()
        print(f"Recommended Restaurants before annotations: {recommended_restaurants}")

        recommended_restaurants = recommended_restaurants.annotate(
            avg_rating=Avg('reviews__rating'),
            no_of_reviews=Count('reviews')
        ).order_by('-avg_rating', '-no_of_reviews')
        print(f"Recommended Restaurants after annotations: {recommended_restaurants}")

        return recommended_restaurants



class TopRestaurantViewSet(viewsets.ModelViewSet):
    queryset = TopRestaurant.objects.all()
    serializer_class = TopRestaurantSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch user info from Google using the access token
        try:
            user_info_response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                # https://openidconnect.googleapis.com/v1/userinfo
                headers={'Authorization': f'Bearer {token}'}
            )
            user_info_response.raise_for_status()
            user_info = user_info_response.json()
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Failed to fetch user info from Google', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        google_id = user_info.get('sub')
        email = user_info.get('email')
        profile_picture = user_info.get('picture')
        username = user_info.get('name')

        if not google_id or not email:
            return Response({'error': 'Incomplete user info from Google'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = CustomUser.objects.get_or_create(
            google_id=google_id,
            defaults={
                'username': username,
                'email': email,
                'profile_picture': profile_picture,
            }
        )

        if created:
            user.set_unusable_password()
            user.save()

        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GoogleLoginTestView(APIView):
    def post(self, request):
        # Log the request data for debugging purposes
        print("Request received with data:", request.data)

        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Simulate a successful response
        user_data = {
            'id': 'test_user_id',
            'username': 'test_user',
            'email': 'test_user@example.com',
            'profile_picture': 'http://example.com/test_user.jpg'
        }
        return Response(user_data, status=status.HTTP_200_OK)
    
class CreateReviewAPIView(APIView):
    def post(self, request):
        serializer = CreateReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.create_or_update_review(serializer.validated_data)
            return Response(CreateReviewSerializer(review).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserReviewsAPIView(APIView):
    def get(self, request, user_id):
        reviews = Review.objects.filter(user_id=user_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class AddToFavoritesAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        restaurant_id = request.data.get('restaurant_id')

        try:
            user = CustomUser.objects.get(id=user_id)
            restaurant = Restaurant.objects.get(id=restaurant_id)

            if restaurant not in user.favorite_restaurants.all():
                user.favorite_restaurants.add(restaurant)
                user.save()
                print(f"{restaurant.name} added to favorites for user {user.username}")
                return Response({'message': 'Restaurant added to favorites'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Restaurant already in favorites'}, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)


class RemoveFromFavoritesAPIView(APIView):

    def post(self, request):
        user_id = request.data.get('user_id')
        restaurant_id = request.data.get('restaurant_id')

        try:
            user = CustomUser.objects.get(id=user_id)
            restaurant = Restaurant.objects.get(id=restaurant_id)

            if restaurant in user.favorite_restaurants.all():
                user.favorite_restaurants.remove(restaurant)
                user.save()
                print(f"{restaurant.name} removed from favorites for user {user.username}")
                return Response({'message': 'Restaurant removed from favorites'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Restaurant not in favorites'}, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)


class FavoriteRestaurantsAPIView(APIView):

    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            favorite_restaurants = user.favorite_restaurants.all()
            print(f"Favorite restaurants for user {user_id}: {favorite_restaurants}")
            serializer = FavoriteRestaurantSerializer(favorite_restaurants, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class AddRestaurantView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        # Extract user ID
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare restaurant data(pickle buffer vanne kura namilera gareko i don't know what it means)
        restaurant_data = {
            'name': request.data.get('name'),
            'location': request.data.get('location'),
            'description': request.data.get('description'),
            'opening_hours': request.data.get('opening_hours'),
            'price': request.data.get('price'),
            'user': user_id,
        }

        # restaurant instance without images
        serializer = AddRestaurantSerializer(data=restaurant_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        restaurant = serializer.save()

        #Multiple image hune vayeko le process gareko
        menu_images = []
        for key, file in request.FILES.items():
            if key.startswith('menu_'):
                menu_image = MenuImage.objects.create(image=file)
                menu_images.append(menu_image.id)

        # Image lai restaurant sanga associate garne
        restaurant.menu_images.set(menu_images)
        restaurant.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserRequestedRestaurantsAPIView(generics.ListAPIView):
    serializer_class = AddRestaurantSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        
        if not user_id:
            return AddRestaurant.objects.none()
        
        try:
            return AddRestaurant.objects.filter(user_id=user_id)
        except Exception as e:
            print(f"Error fetching requested restaurants: {e}")
            return AddRestaurant.objects.none()