from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.dispatch import receiver

from cart.models import Payment, Product


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


@receiver(post_save, sender=Payment)
def payment_made(sender, instance, created, **kwargs):
    if not created:
        for item in iter(kwargs.get('update_fields')):
            if item == 'successful' and instance.successful == True:
                print('Payment passed')


post_save.connect(payment_made, sender=Payment)

pre_save.connect(pre_save_product_receiver, sender=Product)
