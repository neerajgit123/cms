
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework.decorators import api_view
from rest_framework import serializers
from .models import  User, Post, Like

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2', 'name' ,'first_name', 'last_name', 'profile', 'gender')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            gender=validated_data['gender'],
            profile=validated_data['profile'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name','first_name', 'last_name', 'profile', 'gender')
      
class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id', 'title', 'publish', 'content', 'user', 'picture', 'description', 'creation_date', 'like_count', 'dislike_count')
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['user'] =  instance.user.name
        return data
    
    def get_like_count(self, obj):
        return obj.like_post.filter(is_soft_deleted=False).count()

    def get_dislike_count(self, obj):
        return obj.like_post.filter(is_soft_deleted=True).count()
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'post', 'user')
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['user'] =  instance.user.name
        data['post'] =  instance.post.title
        return data