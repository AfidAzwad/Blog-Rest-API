from rest_framework import permissions


class BlogIsCreatedByOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of a blogpost
        return obj.created_by == request.user


class CommentIsCreatedByOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of a blogpost
        return obj.comment_by == request.user