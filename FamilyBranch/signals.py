from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Person


@receiver(pre_save, sender=Person)
def enforce_gender_constraint(sender, instance, **kwargs):
    if instance.father and instance.father.gender != Person.Gender.MALE:
        raise ValueError("Father must be a male")

    if instance.mother and instance.mother.gender != Person.Gender.FEMALE:
        raise ValueError("Mother must be a female")
