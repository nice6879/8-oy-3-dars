from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Product
from .serializers import CartSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({"detail": "User already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user, active=True)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user, active=True)
        product_code = request.data.get('product_code')
        product = Product.objects.filter(code=product_code).first()

        if not product:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

class RemoveProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user, active=True)
        product_code = request.data.get('product_code')
        all_remove = request.data.get('all', False)

        product = Product.objects.filter(code=product_code).first()
        if not product:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            if all_remove or cart_item.quantity == 1:
                cart_item.delete()
            else:
                cart_item.quantity -= 1
                cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

