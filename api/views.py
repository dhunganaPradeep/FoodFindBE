# Django imports
from django.db.models import Count, Q, Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Django Rest Framework imports
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

# Google authentication imports
from google.auth.transport import requests
from google.oauth2 import id_token

# Model imports
from .models import Restaurant, TopRestaurant, CustomUser, Tag, Review

# Serializer imports
from .serializers import (
    AddRestaurantSerializer,
    CreateReviewSerializer,
    CustomUserSerializer,
    FavoriteRestaurantSerializer,
    RestaurantDetailSerializer,
    RestaurantListSerializer,
    ReviewSerializer,
    TagSerializer,
    TopRestaurantSerializer
)

# Other imports
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
        recommend = self.request.query_params.get('recommend', 'false').lower() == 'true'
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
        user_favorites = user.favorite_restaurants.all()
        user_reviews = Review.objects.filter(user=user)

        similar_users = CustomUser.objects.filter(
            Q(favorite_restaurants__in=user_favorites) |
            Q(reviews__restaurant__in=[review.restaurant for review in user_reviews])
        ).exclude(id=user.id).distinct()

        collaborative_recommendations = Restaurant.objects.filter(
            Q(favorited_by__in=similar_users) |
            Q(reviews__user__in=similar_users)
        ).exclude(
            Q(favorited_by=user) |
            Q(reviews__user=user)
        ).distinct()

        user_tags = Tag.objects.filter(restaurants__in=user_favorites).distinct()
        content_recommendations = Restaurant.objects.filter(tags__in=user_tags).exclude(
            Q(favorited_by=user) |
            Q(reviews__user=user)
        ).distinct()

        recommended_restaurants = (collaborative_recommendations | content_recommendations).distinct()

        recommended_restaurants = recommended_restaurants.annotate(
            avg_rating=Avg('reviews__rating'),
            no_of_reviews=Count('reviews')
        ).order_by('-avg_rating', '-no_of_reviews')

        if not recommended_restaurants.exists():
            return Restaurant.objects.all()
        
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

        # Return user info without creating a session
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
    def post(self, request, *args, **kwargs):
        serializer = AddRestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AddRestaurantView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.data.get('user_id')
        serializer = AddRestaurantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
