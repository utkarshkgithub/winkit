from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'price', 'subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_status', 'total_amount', 'created_at']
    list_filter = ['order_status', 'created_at']
    search_fields = ['user__username', 'user__email', 'shipping_address']
    list_editable = ['order_status']
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'order_status', 'total_amount')
        }),
        ('Shipping Details', {
            'fields': ('shipping_address', 'phone_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'price', 'subtotal']
    list_filter = ['created_at']
    search_fields = ['product_name', 'order__user__username']
    readonly_fields = ['subtotal']
