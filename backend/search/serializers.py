from rest_framework import serializers
from .models import Paper, Author, Keyword

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'department_name']

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['name']

class PaperSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    keywords = KeywordSerializer(many=True)
    class Meta:
        model = Paper
        fields = ('title', 'authors', 'published_date', 'abstract', 'link', 'crawl_time', 'keywords')
