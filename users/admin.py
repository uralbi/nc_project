from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from .models import *
from .forms import ProductForm

class UserViewAdmin(admin.ModelAdmin):
    form = User
    list_display = ('id', 'username', 'email', 'phone')

class SCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_category',)
    list_editable = ('sub_category',)


class MCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'main_category')


class ProductAdmin (admin.ModelAdmin):
    form = ProductForm
    list_display = ('id', 'username', 'product', 'city', 'price', 'description', 'main_category', 'sub_category', 'created_at', 'updated_at',
                    'photo1', 'photo2','photo3', 'photo4',  'views')
    list_editable = ('sub_category',)
    list_display_links = ('id', 'product',)
    search_fields = ('product', 'description', 'city')

admin.site.site_title = 'Admin'
admin.site.site_header = 'Admin'

# Unregister the provided model admin
admin.site.unregister(User)
admin.site.register(Products, ProductAdmin)
admin.site.register(SubCategory, SCategoryAdmin)
admin.site.register(MainCategory, MCategoryAdmin)

# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email')