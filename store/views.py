from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Customer, Order, OrderItem  
from .forms import RegisterForm, LoginForm
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages 
from .models import User, Product, Category, Customer, Order, OrderItem  
from django.db.models import Sum
from .serializers import (
    ProductSerializer, CategorySerializer, CustomerSerializer, OrderSerializer,
    RegisterSerializer, LoginSerializer
)


@login_required(login_url='login-user')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = [{'product': p, 'quantity': cart[str(p.id)]} for p in products]
    return render(request, 'cart.html', {'cart_items': cart_items})



def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() 
            Customer.objects.create(user=user)  
            messages.success(request, 'Your account has been created successfully. You can now log in.')
            return redirect('login-user')
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                messages.success(request, 'Welcome back! You have logged in successfully.')
                
                if user.role == 'Admin':
                    return redirect('admin-dashboard')
                else:
                    return redirect('customer-dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def dashboard(request):
    if request.user.is_staff:
        return redirect('admin-dashboard')
    return redirect('customer-dashboard')


def checkout(request):
   
    if not isinstance(request.user, User):
        messages.error(request, "An unexpected error occurred.")
        return redirect('login-user')

    try:
       
        customer = Customer.objects.get(user=request.user)
        cart_items = OrderItem.objects.filter(order__customer=customer, order__status='Pending')
        total_price = sum(item.price_per_unit * item.quantity for item in cart_items)
        return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})
    except Customer.DoesNotExist:
        
        messages.error(request, "You must complete your profile information before proceeding to checkout.")
        return redirect('profile')

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email
        })

class CustomerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user.customer  
        orders = Order.objects.filter(customer=customer)
        return Response({
            'total_orders': orders.count(),
            'order_history': [order.id for order in orders],
        })

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:  
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        total_orders = Order.objects.count()
        total_sales = Order.objects.filter(status='Delivered').aggregate(Sum('total_price'))['total_price__sum']
        pending_orders = Order.objects.filter(status='Pending').count()

        return Response({
            'total_orders': total_orders,
            'total_sales': total_sales,
            'pending_orders': pending_orders
        })
