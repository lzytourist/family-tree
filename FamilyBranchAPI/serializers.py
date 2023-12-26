from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import Person


class PersonRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'dob', 'gender', 'age']


class PersonSerializer(serializers.ModelSerializer):
    father_id = serializers.IntegerField(write_only=True, required=False)
    mother_id = serializers.IntegerField(write_only=True, required=False)
    father = PersonRelationSerializer(read_only=True)
    mother = PersonRelationSerializer(read_only=True)

    class Meta:
        model = Person
        fields = ['id', 'name', 'gender', 'dob', 'date_of_death', 'age', 'nationality', 'father', 'mother', 'father_id',
                  'mother_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'age': {'read_only': True},
            'id': {'read_only': True},
            'date_of_death': {'write_only': True}
        }

    def create(self, validated_data):
        try:
            validated_data['user_id'] = self.context['request'].user.pk
            return super().create(validated_data)
        except ValueError as ve:
            raise serializers.ValidationError(str(ve))


class CustomUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        return super().create(validated_data)
