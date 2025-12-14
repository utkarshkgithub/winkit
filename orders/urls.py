from django.urls import path
from .views import (
    CreateOrderView,
    OrderDetailView,
    UserOrdersView,
    UpdateOrderStatusView,
    TimelineView
)

app_name = 'orders'

urlpatterns = [
    path('', CreateOrderView.as_view(), name='create'),
    path('<int:order_id>', OrderDetailView.as_view(), name='detail'),
    path('user/<int:user_id>', UserOrdersView.as_view(), name='user_orders'),
    path('<int:order_id>/status', UpdateOrderStatusView.as_view(), name='update_status'),
    path('<int:order_id>/timeline', TimelineView.as_view(), name='timeline'),
]
