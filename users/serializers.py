from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from .models import Group


UserModel = get_user_model()


class UserDetailsSerializer(UserDetailsSerializer):
    """
    User model w/o password
    """

    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, 'display_name'):
            extra_fields.append('display_name')
        if hasattr(UserModel, 'avatar_url'):
            extra_fields.append('avatar_url')
        model = UserModel
        fields = ('id', *extra_fields)
        read_only_fields = ('id', *extra_fields)


class UserSerializer(serializers.ModelSerializer):
    """
        This serializer is for serializing User Models
    """
    avatar_url = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'first_name', 'last_name', 'email', 'furigana_lname', 'furigana_fname',
            'position', 'avatar_url', 'date_joined', 'display_name'
        )
        read_only_fields = (
            'id', 'display_name'
        )


class OwnerUserSerializer(serializers.ModelSerializer):
    """
        This serializer is for serializing User Models
    """
    avatar_url = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model = get_user_model()
        fields = (
            'id', 'first_name', 'last_name', 'email', 'furigana_lname', 'furigana_fname',
            'position', 'avatar_url', 'date_joined', 'display_name'
        )
        read_only_fields = (
            'id', 'display_name', 'date_joined'
        )


class GroupSerializer(serializers.ModelSerializer):
    """
        This serializer is for serializing User Models
    """
    class Meta:
        model = Group
        fields = (
            'id', 'name',
        )
        read_only_fields = (
            'id', 'name',
        )
