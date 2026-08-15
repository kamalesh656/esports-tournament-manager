from rest_framework import serializers
from .models import User, Team


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'player'),
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')

class TeamSerializer(serializers.ModelSerializer):
    captain_username = serializers.ReadOnlyField(source='captain.username')

    class Meta:
        model = Team
        fields = ('id', 'name', 'captain', 'captain_username', 'created_at')
        read_only_fields = ('captain',)