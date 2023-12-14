from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model


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
