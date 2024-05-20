from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from user.models import UserAccount
from djoser.serializers import UserSerializer

# Tạo một custom serializer kế thứa từ UserCreateSerializer
class UserAccountSerializer(UserCreateSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    class Meta(UserCreateSerializer.Meta):
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'phone', 'address','username')
class UserAccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('username','email','first_name', 'last_name', 'email', 'phone', 'address')
class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserAccount  # Tham chiếu đến model người dùng tùy chỉnh của bạn
        fields = tuple(UserCreateSerializer.Meta.fields) + ('id', 'email','address', 'phone', 'first_name', 'last_name')
