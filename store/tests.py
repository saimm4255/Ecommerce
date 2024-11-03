from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, User

class ProductTests(APITestCase):
    def setUp(self):
       
        self.user = User.objects.create_user(username='admin', password='pass', role='Admin')
        self.client.login(username='admin', password='pass')

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'name': 'Sample Product',
            'description': 'A test product',
            'price': 100.0,
            'stock_quantity': 10
        }
        
        response = self.client.post(url, data, format='json')
        
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
