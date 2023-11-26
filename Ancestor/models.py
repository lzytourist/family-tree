from collections.abc import Iterable
from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class Gender(models.enums.TextChoices):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

class Person(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, db_index=True)
    gender = models.CharField(max_length=8, choices=Gender.choices, default=Gender.MALE)
    dob = models.DateField(null=True, blank=True, verbose_name='Date of birth')
    dod = models.DateField(null=True, blank=True, verbose_name='Date of death')
    nationality = models.CharField(max_length=30, null=True, blank=True)
    # additional_info = models.TextField(null=True, blank=True)

    @property
    def age(self):
        if not self.dod:
            return relativedelta(date.today(), self.dob).years
        return relativedelta(self.dod, self.dob).years
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'

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

    def __str__(self) -> str:
        relation = f"{self.parent.name} is the "
        relation += "father " if self.parent.gender == "male" else "mother "
        relation += f"of {self.children.name}"
        return relation

    def clean(self) -> None:
        if ParentChildren.objects.filter(parent=self.children).filter(children=self.parent).exists():
            raise ValidationError("Reverse relation exists")
        return super().clean()

    class Meta:
        verbose_name = 'Parent Children'
        unique_together = ('parent', 'children',)
