from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, CustomerDashboardView, AdminDashboardView

urlpatterns = [
   
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/customer/', CustomerDashboardView.as_view(), name='customer-dashboard'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
]
