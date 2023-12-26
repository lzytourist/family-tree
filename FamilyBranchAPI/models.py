from datetime import date
from dateutil.relativedelta import relativedelta

from django.db import models
from django.contrib.auth import get_user_model


class Person(models.Model):
    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    name = models.CharField(max_length=150)
    dob = models.DateField(null=True, blank=True, verbose_name='Date of birthday')
    gender = models.CharField(max_length=10, choices=Gender.choices, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    father = models.ForeignKey(
        to='self',
        related_name='children_as_father',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    mother = models.ForeignKey(
        to='self',
        related_name='children_as_mother',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def age(self):
        if not self.date_of_death:
            return relativedelta(date.today(), self.dob).years
        return relativedelta(self.date_of_death, self.dob).years

    @property
    def is_dead(self):
        return self.date_of_death is not None

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
