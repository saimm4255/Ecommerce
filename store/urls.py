from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, CustomerViewSet, OrderViewSet,
    RegisterView, LoginView, LogoutView, ProfileView, CustomerDashboardView, AdminDashboardView,
    product_list, product_detail, cart_view, register_user, login_user, dashboard, checkout
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
  
    path('api/', include(router.urls)),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/profile/', ProfileView.as_view(), name='profile'),
    path('api/dashboard/customer/', CustomerDashboardView.as_view(), name='customer-dashboard'),
    path('api/dashboard/admin/', AdminDashboardView.as_view(), name='admin-dashboard'),

  
    path('', product_list, name='product-list'),
    path('product/<int:product_id>/', product_detail, name='product-detail'),
    path('cart/', cart_view, name='cart'),
    path('auth/register/', register_user, name='register-user'),
    path('auth/login/', login_user, name='login-user'),
    path('dashboard/', dashboard, name='dashboard'),  
    path('checkout/', checkout, name='checkout'), 
]
