from rest_framework import viewsets
from .models import Restaurant
from .models import TopRestaurant
from rest_framework import generics 
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Tag
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from .serializers import TopRestaurantSerializer
from .serializers import RestaurantListSerializer
from .serializers import RestaurantDetailSerializer
from .serializers import TagSerializer
from .serializers import CreateReviewSerializer
from .serializers import ReviewSerializer
from .serializers import FavoriteRestaurantSerializer
from .serializers import AddRestaurantSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import CustomUser
from .models import Review
from .models import AddRestaurant
from .serializers import CustomUserSerializer
import requests

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RestaurantDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.query_params.getlist('tags')

        if tags:
            # Annotate the queryset with the count of matching tags 
            queryset = queryset.annotate(
                matching_tags_count=Count(
                    'tags', filter=Q(tags__name__in=tags))
            ).order_by('-matching_tags_count', 'id')

        return queryset


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
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.data.get('user_id')
        serializer = AddRestaurantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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