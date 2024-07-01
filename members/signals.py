from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Class, Attendance

@receiver(pre_save, sender=Class)
def delete_attendances_if_class_not_available(sender, instance, **kwargs):
    if instance.pk:
        original_instance = Class.objects.get(pk=instance.pk)
        if original_instance.is_available_this_week and not instance.is_available_this_week and not original_instance.finished and not instance.finished:
            Attendance.objects.filter(class_attended=instance).delete()
