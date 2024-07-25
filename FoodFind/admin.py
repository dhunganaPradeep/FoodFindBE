from django import forms
from django.contrib import admin
from django.utils.html import format_html
from api.models import Restaurant, RestaurantImage, Menu, CustomUser, Review, AddRestaurant


# Restaurant Page
class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1

class MenuInline(admin.TabularInline):
    model = Menu
    extra = 1

class RestaurantAdminForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        # Check if the instance has been saved (has a primary key)
        if self.instance.pk:
            images = self.instance.images.all()
            menu_items = self.instance.menu_items.all()

            if not images or not menu_items:
                raise forms.ValidationError("Please add at least one image and one menu item.")
        else:
            # Handle case where instance is not yet saved
            pass

class RestaurantAdmin(admin.ModelAdmin):
    form = RestaurantAdminForm
    inlines = [RestaurantImageInline, MenuInline]
    list_display = ('name', 'location', 'view_details')

    def view_details(self, obj):
        return format_html('<a href="{}">{}</a>', obj.id, 'View Details')
    view_details.short_description = 'View Details' 


# Restaurant Images
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ('restaurant_name', 'image_tag')

    def restaurant_name(self, obj):
        return obj.restaurant.name

    def image_tag(self, obj):
        return f'{obj.image.url}'

    image_tag.short_description = 'Image'
    image_tag.allow_tags = False


# Menus
class MenuAdmin(admin.ModelAdmin):
    list_display = ('restaurant_name', 'name', 'price', 'category', 'edit')
    list_filter = ('restaurant__name', 'category')
    list_select_related = ('restaurant',)

    def restaurant_name(self, obj):
        return obj.restaurant.name
    restaurant_name.short_description = 'Restaurant'

    def edit(self, obj):
        return format_html('<a href="{}">{}</a>', obj.id, 'Edit')
    edit.short_description = 'Modify' 


# User Page
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'view_user_details')
    search_fields = ('username', 'email')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Exclude superusers from the queryset
        return queryset.exclude(is_superuser=True)

    def view_user_details(self, obj):
        return format_html('<a href="{}">{}</a>', obj.id, 'View Details')
    view_user_details.short_description = 'View Details' 


# Review Page
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant_name', 'user_name', 'rating', 'review_text', 'created_at', 'edit')
    list_filter = ('restaurant__name', 'created_at')
    list_select_related = ('restaurant',)

    def restaurant_name(self, obj):
        return obj.restaurant.name
    restaurant_name.short_description = 'Restaurant'

    def user_name(self, obj):
        return obj.user.username
    user_name.short_description = 'Reviewed By'

    def rating(self, obj):
        return obj.rating
    rating.short_description = 'Rating'

    def review_text(self, obj):
        return obj.review_text
    review_text.short_description = 'Review'

    def created_at(self, obj):
        return obj.created_at
    created_at.short_description = 'Created At'

    def edit(self, obj):
        return format_html('<a href="{}">{}</a>', obj.id, 'Edit')
    edit.short_description = 'Modify' 


# admin.py
class AddRestaurantRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'location', 'description', 'opening_hours', 'edit')
    search_fields = ('name', 'location', 'description', 'user__username')

    def edit(self, obj):
        return format_html('<a href="{}">{}</a>', obj.id, 'Edit')
    edit.short_description = 'Modify' 

admin.site.register(AddRestaurant, AddRestaurantRequestAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(RestaurantImage, RestaurantImageAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(CustomUser, CustomUserAdmin)