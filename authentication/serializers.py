from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    phone_number = serializers.CharField(source='profile.phone_number', allow_null=True)
    address = serializers.CharField(source='profile.address', allow_null=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'phone_number', 'address', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class SignupSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'address']

    def create(self, data):
        password=data.pop('password')
        phone_number = data.pop('phone_number', '')
        address = data.pop('address', '')
        
        user = User.objects.create_user(**data,password=password)
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            address=address
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data['username']
        password = data['password']

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
            data['user'] = user
        else:
            raise serializers.ValidationError("Must include username and password")
        
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'address']
    
    def update(self, instance, validated_data):
        # Extract profile fields
        phone_number = validated_data.pop('phone_number', None)
        address = validated_data.pop('address', None)
        
        # Update User fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        
        # Update UserProfile fields
        profile = instance.profile
        if phone_number is not None:
            profile.phone_number = phone_number
        if address is not None:
            profile.address = address
        profile.save()
        
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user password"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value
    
    def validate_new_password(self, value):
        # Use Django's built-in password validators
        validate_password(value)
        return value
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        return data
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
