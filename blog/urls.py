from django.urls import path
from .views import BlogViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'blog', BlogViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls
