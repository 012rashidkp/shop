from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    userid = serializers.CharField(source='id', read_only=True)
    password = serializers.CharField(max_length=65, min_length=6, write_only=True)
    email = serializers.EmailField(max_length=15, min_length=4),
    city = serializers.CharField(max_length=100, min_length=2)
    phone = serializers.CharField(max_length=10, min_length=2)
    username = serializers.CharField(max_length=150, min_length=2)

    class Meta:
        model = User
        