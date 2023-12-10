from django.db.models.query import Q
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Person, ParentChildren


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'gender', 'dob', 'dod', 'nationality', 'age']
        extra_kwargs = {
            'age': {'read_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.pk
        return super().create(validated_data)


class ParentChildrenSerializer(serializers.ModelSerializer):
    parent = PersonSerializer(read_only=True)
    parent_id = serializers.IntegerField(write_only=True)
    children = PersonSerializer(read_only=True)
    children_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ParentChildren
        fields = ['id', 'parent', 'children', 'parent_id', 'children_id']
        validators = [
            UniqueTogetherValidator(
                queryset=ParentChildren.objects.all(),
                fields=('parent_id', 'children_id',),
                message='Relation already exists'
            )
        ]

    def validate_parent_id(self, value):
        if not Person.objects.filter(user=self.context['request'].user).filter(pk=value).exists():
            raise serializers.ValidationError("Parent does not exists")
        return value

    def validate_children_id(self, value):
        if not Person.objects.filter(user=self.context['request'].user).filter(pk=value).exists():
            raise serializers.ValidationError("Children does not exists")
        return value

    def validate(self, attrs):
        if attrs['parent_id'] == attrs['children_id']:
            raise serializers.ValidationError("Invalid parent or children")
        if ParentChildren.objects.filter(
                Q(parent_id=attrs['children_id']) & Q(children_id=attrs['parent_id'])).exists():
            raise serializers.ValidationError("Reverse relation exists")

        return super().validate(attrs)
