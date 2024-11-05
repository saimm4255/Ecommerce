from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Product, User

class AuthTests(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'pass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'pass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class DashboardTests(APITestCase):
    def test_customer_dashboard(self):
        self.user = User.objects.create_user(username='customer', password='pass123', role='Customer')
        self.client.login(username='customer', password='pass123')

        url = reverse('customer-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_dashboard(self):
        self.user = User.objects.create_user(username='admin', password='pass123', is_staff=True)
        self.client.login(username='admin', password='pass123')

        url = reverse('admin-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)




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