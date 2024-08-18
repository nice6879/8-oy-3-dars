from django.urls import path
from .views import CartView, AddProductView, RemoveProductView
from .views import RegisterView, LogoutView 

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('add-product/', AddProductView.as_view(), name='add_product'),
    path('remove-product/', RemoveProductView.as_view(), name='remove_product'),
    path('register/', RegisterView.as_view(), name='register'),
    path('log-out/', LogoutView.as_view(), name='log_out'),
]
