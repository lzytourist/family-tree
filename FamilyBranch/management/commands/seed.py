from django.core.management.base import BaseCommand
from FamilyBranch.models import Person


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        # Your seeding logic goes here
        self.stdout.write(self.style.SUCCESS('Seeding data...'))

        Person.objects.all().delete()

        father = Person.objects.create(
            name='Asfak Ali Khan',
            gender=Person.Gender.MALE,
            nationality='Bangladeshi',
            user_id=1
        )
        mother = Person.objects.create(
            name='Nasrin Akter',
            gender=Person.Gender.FEMALE,
            nationality='Bangladeshi',
            user_id=1
        )

        Person.objects.create(
            name='Monowar Hossain Khan',
            gender=Person.Gender.MALE,
            nationality=father.nationality,
            father=father,
            mother=mother,
            user_id=1
        )

        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully'))
