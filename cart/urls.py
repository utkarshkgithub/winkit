from django.urls import path
from .views import AddToCartView, UpdateCartView, GetCartView, ClearCartView

app_name = 'cart'

urlpatterns = [
    path('add', AddToCartView.as_view(), name='add'),
    path('update', UpdateCartView.as_view(), name='update'),
    path('', GetCartView.as_view(), name='get'),
    path('clear', ClearCartView.as_view(), name='clear'),
]
