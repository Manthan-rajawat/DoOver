from rest_framework import serializers
from .models import CustomUser

class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = ['id', 'email', 'username']
        read_only_fields = ['id']

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model =CustomUser
        fields = ['email','username','password','confirm_password']
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords don't match"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(username=validated_data['username'],email=validated_data['email'],password=validated_data['password'])
        return user
       
class LoginSerializer (serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    class Meta:
        model = CustomUser
        fields = ['username','password']

class UserUpdateSerializer (serializers.ModelSerializer):
    username = serializers.CharField(required=True,)
    email = serializers.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = ['username','email']



class ChangePasswordSerializer (serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = CustomUser
        fields = ['password','confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords don't match"})
        return data
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
        
