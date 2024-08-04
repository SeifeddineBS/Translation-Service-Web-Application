from rest_framework import serializers
from .models import Translation
from django.contrib.auth.models import User

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['id','original_text','translated_text','type','user']


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password', 'email']