import random

from faker import Faker

from FamilyBranch.models import Person

fake = Faker()


class PersonFactory:
    def __init__(self, user, depth):
        self.user = user

        self.root_person = self.create_person()
        self.root_person.save()

        print('Creating family for: ', self.root_person.name)
        self.create_family(depth=depth, parent=self.root_person)

    def create_person(self, father=None, mother=None):
        person = Person(
            user=self.user,
            name=fake.name(),
            dob=fake.date_of_birth(),
            gender='male',
            nationality='Bangladeshi',
            father=father,
            mother=mother
        )
        return person

    def create_children(self, father=None, mother=None):
        children = []
        for i in range(random.randrange(1, 5)):
            children.append(self.create_person(father, mother))
        return Person.objects.bulk_create(children)

    def create_family(self, depth, parent=None):
        print(depth)
        if depth <= 0:
            return None

        children = self.create_children(father=parent)
        for child in children:
            print('Creating children for: ', child)
            self.create_family(depth - 1, parent=child)
            # self.create_family(depth - 1)
