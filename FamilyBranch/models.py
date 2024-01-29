from datetime import date
from dateutil.relativedelta import relativedelta
from os.path import isfile

from django.db import models
from django.contrib.auth import get_user_model
from faker import Faker, Factory
from PIL import Image


class PersonManager(models.Manager):
    def get_root_ancestor(self, person_id):
        query = """
        WITH RECURSIVE Ancestors AS (
            SELECT id, name, father_id, mother_id, gender
            FROM FamilyBranch_person
            WHERE id = %s

            UNION

            SELECT p.id, p.name, p.father_id, p.mother_id, p.gender
            FROM FamilyBranch_person p
            JOIN Ancestors a ON p.id = a.father_id OR p.id = a.mother_id
        )
        SELECT *
        FROM Ancestors
        WHERE father_id IS NULL AND mother_id IS NULL
        ORDER BY gender DESC
        LIMIT 1
        """

        return self.raw(query, [person_id])[0]


class Person(models.Model):
    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    name = models.CharField(max_length=150)
    dob = models.DateField(null=True, blank=True, verbose_name='Date of birthday')
    gender = models.CharField(max_length=10, choices=Gender.choices, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='static/person_images/', null=True, blank=True)
    child_no = models.PositiveSmallIntegerField(null=True, blank=True, default=1)

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

    objects = PersonManager()

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image is not None:
            try:
                img = Image.open(self.image.path)

                aspect_ratio = img.width / img.height
                height = 300
                width = round(aspect_ratio * height)

                resized_img = img.resize((width, height))
                resized_img.save(self.image.path)
            except ValueError:
                pass

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
