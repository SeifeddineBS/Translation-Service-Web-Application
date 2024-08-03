from rest_framework import serializers
from .models import Translation
class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['id','original_text','translated_text','type','user']