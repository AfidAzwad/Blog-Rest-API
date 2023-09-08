from rest_framework import serializers
from .models import BlogPost, BlogComment
from user.models import User

class BlogCommentSerializer(serializers.ModelSerializer):
    comment_by_email = serializers.SerializerMethodField()  # Custom field for created_by email

    class Meta:
        model = BlogComment
        fields = ('id', 'blogpost', 'body', 'comment_by', 'comment_by_email', 'created', 'modified')
        
    def get_comment_by_email(self, obj):
        return obj.comment_by.email if obj.comment_by else None

class BlogPostSerializer(serializers.ModelSerializer):
    comments = BlogCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'description', 'status', 'created_by', 'created', 'modified', 'comments')
        

