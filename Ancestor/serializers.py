from rest_framework import serializers

from .models import Person, ParentChildren

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'gender', 'dob', 'dod', 'nationality', 'age']

        extra_kwargs = {
            'age': {'read_only': True}
        }

class ParentChildrenSerializer(serializers.ModelSerializer):
    parent = PersonSerializer()
    parent_id = serializers.IntegerField()
    children = PersonSerializer()
    children_id = serializers.IntegerField()

    class Meta:
        model = ParentChildren
        fields = ['parent', 'children', 'parent_id', 'children_id']
        extra_kwargs = {
            'parent': {'read_only': True},
            'parent_id': {'write_only': True},
            'children': {'read_only': True},
            'children_id': {'write_only': True}
        }
