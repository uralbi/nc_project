from ast import Sub
from django.test import TestCase
from django.urls import reverse
import pytest
from users.models import Products, MainCategory, SubCategory
from django.contrib.auth.models import User


def test_homepage_accesss():
    url = reverse('home')
    assert url == '/'

def test_login_access():
    url = reverse('login')
    assert url == '/login/'

def test_register_access():
    url = reverse('register')
    assert url == '/register/'

def test_post_access():
    url = reverse('post_product')
    assert url == '/post/'


@pytest.fixture
def new_product(db):
    product = Products.objects.create(
        username = User.objects.create(username = 'test_user', email = 'test@gmail.com', password = 'asdfqwer'),
        product = 'New Macbook Pro',
        price = '890',
        description = "New",
        main_category = MainCategory.objects.create(main_category = 'Test_c'),
        sub_category = SubCategory.objects.create(sub_category='Computers')
    )
    return product


@pytest.fixture
def new_product_2(db):
    product = Products.objects.create(
        username = User.objects.create(username = 'test_user2', email = 'test2@gmail.com', password = 'asdfqwer'),
        product = 'LG Monitor FHD',
        price = '250',
        description = "New",
        main_category = MainCategory.objects.create(main_category = 'Test_c'),
        sub_category = SubCategory.objects.create(sub_category='Computers')
    )
    return product

def test_search_product(new_product):
    assert Products.objects.filter(product="New Macbook Pro").exists()


def test_update_product(new_product):
    new_product.product = 'Used Macbook'
    new_product.save()
    assert Products.objects.filter(product='Used Macbook').exists()


def test_compare_products(new_product, new_product_2):
    assert new_product.pk != new_product_2.pk


@pytest.fixture
def test_user(db, django_user_model):
    django_user_model.objects.create_user(
        username="test_user3", password="test_password")
    return "test_user3", "test_password"

def test_login_user(client, test_user):
    test_username, test_password = test_user  # this unpacks the tuple
    login_result = client.login(username=test_username, password=test_password)
    assert login_result == True