from datetime import date

from django.db import models
from django.contrib.auth.models import User


class Gender(models.enums.TextChoices):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

class Person(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    gender = models.CharField(max_length=8, choices=Gender.choices, default=Gender.MALE)
    dob = models.DateField(null=True, blank=True)
    dod = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)
    # additional_info = models.TextField(null=True, blank=True)

    @property
    def age(self):
        if not self.dod:
            return (date.today() - self.dob).days
        return (self.dod - self.dob).days
    
    def __str__(self) -> str:
        return self.name

class ParentChildren(models.Model):
    parent = models.ForeignKey(
        to=Person,
        related_name='parent',
        on_delete=models.PROTECT
    )
    children = models.ForeignKey(
        to=Person,
        related_name='children',
        on_delete=models.PROTECT
    )

    class Meta:
        unique_together = ('parent', 'children',)
