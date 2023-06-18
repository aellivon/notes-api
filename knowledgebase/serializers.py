from .models import KnowledgeBase

from rest_framework import serializers


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    """
        This serializer is for serializing User Models
    """
    class Meta:
        model = KnowledgeBase
        fields = (
            'id', 'title', 'description', 'is_public', 'owner'
        )
        read_only_fields = (
            'id', 'owner'
        )
