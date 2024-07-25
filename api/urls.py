from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet
from .views import TopRestaurantViewSet
from .views import TagsViewSet
from .views import GoogleLoginView
from .views import GoogleLoginTestView
from .views import CreateReviewAPIView
from .views import UserReviewsAPIView
from .views import AddToFavoritesAPIView
from .views import RemoveFromFavoritesAPIView
from .views import FavoriteRestaurantsAPIView
from .views import AddRestaurantView
from .views import UserRequestedRestaurantsAPIView


router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'top-restaurants', TopRestaurantViewSet)
router.register(r'tags', TagsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('google-login-test/', GoogleLoginTestView.as_view(), name='google-login-test'),
    path('create-review/', CreateReviewAPIView.as_view(), name='create_review'),
    path('user-reviews/<str:user_id>/', UserReviewsAPIView.as_view(), name='user-reviews'),
    path('add-to-favorites/', AddToFavoritesAPIView.as_view(), name='add_to_favorites'),
    path('remove-from-favorites/', RemoveFromFavoritesAPIView.as_view(), name='remove_from_favorites'),
    path('favorite-restaurants/<int:user_id>/', FavoriteRestaurantsAPIView.as_view(), name='favorite_restaurants'),
    path('add-restaurant/', AddRestaurantView.as_view(), name='add-restaurant'),
    path('user-requested-restaurants/<int:user_id>/', UserRequestedRestaurantsAPIView.as_view(), name='user-requested-restaurants'),
]

