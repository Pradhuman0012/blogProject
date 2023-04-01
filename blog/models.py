from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


from taggit.managers import TaggableManager
class Post(models.Model):
    POST_CHOICES=(('draft','Draft'),('published','Published'))
    title=models.CharField(max_length=150)
    slug=models.SlugField(max_length=264,unique_for_date='publish')
    author=models.ForeignKey(User,related_name='blog_post',on_delete=models.CASCADE)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=POST_CHOICES,default='draft')
    tags=TaggableManager()
    objects=CustomManager()

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.publish.year,self.publish.strftime('%m'),self.slug])
    
    def __str__(self):
            return self.title
    class Meta:
        ordering=('-publish',)


# comment section
class comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Mets:
        ordering=('-created',)
    def __str__(self):
         return f"Commented by {self.name} on {self.post}."