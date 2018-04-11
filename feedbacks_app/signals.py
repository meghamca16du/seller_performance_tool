from .models import Feedbacks
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Feedbacks)
def index_post(sender, instance, **kwargs):
    print(instance)
    instance.indexing()
