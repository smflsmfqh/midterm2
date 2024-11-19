# blog/serializers.py
from rest_framework import serializers
from .models import Post, Image, Comment  

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = '__all__'

    def validate_text(self, value):
        if not value:
            raise serializers.ValidationError("Comment text cannot be empty.")
        return value
    
    # 새로 정의된 create 메서드에서 'author'를 수동으로 설정
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user  # 로그인한 사용자로 author를 설정
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post  
        fields = '__all__'  

