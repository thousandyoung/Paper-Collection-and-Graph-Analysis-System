from rest_framework import serializers
from .models import Spider

class SpiderSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Spider
        fields = ['id', 'name', 'keyword', 'total_pages', 'current_page', 'progress', 'status']
