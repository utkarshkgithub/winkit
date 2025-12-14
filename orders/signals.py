from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Order, OrderStatusHistory


@receiver(pre_save, sender=Order)
def capture_previous_status(sender, instance, **kwargs):
    """Capture the previous status before saving"""
    if instance.pk:
        try:
            previous = Order.objects.get(pk=instance.pk)
            instance._previous_status = previous.order_status
        except Order.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=Order)
def track_order_status_change(sender, instance, created, **kwargs):
    """Automatically create history entry when order is created or status changes"""
    
    if created:
        # Order creation - record initial "pending" status
        OrderStatusHistory.objects.create(
            order=instance,
            old_status=None,
            new_status=instance.order_status,
            changed_by=None,  # System-generated
            notes="Order created"
        )
    elif hasattr(instance, '_previous_status') and instance._previous_status != instance.order_status:
        # Status changed - record the change
        changed_by = getattr(instance, '_changed_by', None)
        OrderStatusHistory.objects.create(
            order=instance,
            old_status=instance._previous_status,
            new_status=instance.order_status,
            changed_by=changed_by,
            notes=getattr(instance, '_change_notes', '')
        )
