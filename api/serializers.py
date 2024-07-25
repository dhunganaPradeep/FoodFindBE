from rest_framework import serializers
from .models import Restaurant
from .models import RestaurantImage
from .models import Review
from .models import Menu
from .models import TopRestaurant
from .models import Tag
from .models import CustomUser
from .models import AddRestaurant


class CustomUserSerializer(serializers.ModelSerializer):
    favorite_restaurants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'profile_picture', 'favorite_restaurants']

        def to_representation(self, instance):
            if instance is not None:
                return super().to_representation(instance)
            else:
                return None

class FavoriteRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location']
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    restaurant_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'review_text', 'created_at', 'updated_at', 'restaurant_name', 'restaurant_id']

    def get_restaurant_name(self, obj):
        return obj.restaurant.name

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'rating', 'review_text', 'restaurant']

    def create_or_update_review(self, validated_data):
        user = validated_data['user']
        restaurant = validated_data['restaurant']
        try:
            review = Review.objects.get(user=user, restaurant=restaurant)
            # If the review exists, update it
            review.rating = validated_data['rating']
            review.review_text = validated_data['review_text']
            review.save()
        except Review.DoesNotExist:
            # If the review does not exist, create it
            review = Review.objects.create(**validated_data)
        return review

    def validate(self, data):
        user = data['user']
        restaurant = data['restaurant']
        
        # Check if a review already exists for the user and restaurant combination
        if Review.objects.filter(user=user, restaurant=restaurant).exists():
            # If a review already exists, return the data without raising a validation error
            return data
        
        return super().validate(data)


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'price','category']


class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = ('id', 'image')


class RestaurantListSerializer(serializers.ModelSerializer):
    images = RestaurantImageSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = fields = ('id', 'name', 'location', 'description', 'images')


class RestaurantDetailSerializer(serializers.ModelSerializer):
    menu_items = MenuSerializer(many=True,read_only=True)
    images = RestaurantImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    menu_items = MenuSerializer(many=True, read_only=True)
    no_of_reviews = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['images', 'id', 'name', 'location', 'price', 'opening_hours', 'description',
                  'average_rating', 'reviews', 'map_url', 'menu_items', 'no_of_reviews', 'tags','menu_items']

    def get_no_of_reviews(self, obj):
        return obj.no_of_reviews()

    def get_average_rating(self, obj):
        return obj.average_rating()


class TopRestaurantSerializer(serializers.ModelSerializer):
    restaurant = RestaurantListSerializer(read_only=False)

    class Meta:
        model = TopRestaurant
        fields = ['id', 'restaurant', 'restaurant', 'ranking']


class AddRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddRestaurant
        fields = ['user', 'name', 'location', 'description', 'opening_hours', 'price', 'menu']
