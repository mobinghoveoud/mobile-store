from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from mobiles.models import Variant


@receiver(post_delete, sender=Variant)
def auto_delete_image_on_delete(sender, instance: Variant, **kwargs):
    instance.image.delete(save=False)


@receiver(pre_save, sender=Variant)
def auto_delete_image_on_change(sender, instance: Variant, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Variant.objects.get(pk=instance.pk).image
    except Variant.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        try:
            old_file.delete()
        except Exception:
            pass
