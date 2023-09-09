from django.db import models
from user.models import User

STATUS_CHOICES =(
    ("draft", "Draft"),
    ("published", "Published"),
)

class BlogPost(models.Model):
    title = models.CharField('Title', max_length=200)
    description = models.TextField('Description')
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return self.title

class BlogComment(models.Model):
    blogpost = models.ForeignKey(BlogPost, related_name='Comments', on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User, verbose_name='Commented By', on_delete=models.CASCADE)
    body = models.TextField('Body')
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created']

    def __str__(self):
        return '%s: %s' % (self.comment_by.email, self.body)

    
