from rest_framework import serializers
from .models import Manhwa, Chapter, ChapterPage

class ChapterPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterPage
        fields = ['id', 'image']  # Add any other fields as necessary

class ChapterSerializer(serializers.ModelSerializer):
    pages = ChapterPageSerializer(many=True, read_only=True)  # Embed pages in the chapter serializer

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'pdf_file', 'pages']

class ManhwaSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Manhwa
        fields = ['id', 'title', 'description', 'cover_image', 'chapters']
