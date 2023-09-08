from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import BlogPostSerializer, BlogCommentSerializer
from .models import BlogPost, BlogComment
from rest_framework.permissions import IsAuthenticated
from .permissions import BlogIsCreatedByOrReadonly, CommentIsCreatedByOrReadonly
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class BlogViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    permission_classes = [IsAuthenticated, BlogIsCreatedByOrReadonly]
    serializer_class = BlogPostSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Enable search and ordering
    search_fields = ['title', 'status', 'created_by__email']  # Fields to search
    ordering_fields = ['created']  # Fields for ordering
    
    pagination_class = PageNumberPagination
    page_size = 5
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = BlogPostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not BlogIsCreatedByOrReadonly().has_permission(request, self):
            return Response({"detail": "You do not have permission to update this object."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    


class CommentViewSet(viewsets.ModelViewSet):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    permission_classes = [IsAuthenticated, CommentIsCreatedByOrReadonly]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['comment_by'] = request.user.id
        serializer = BlogCommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    