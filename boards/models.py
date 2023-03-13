from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
# Create your models here.

class Board(models.Model):

    name = models.CharField(max_length=50, null=True, unique=True)
    description = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name
    
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()
    
    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by("created_at").last()
    
class Topic(models.Model):

    subject = models.CharField(max_length=50, null=True)
    board = models.ForeignKey(Board, related_name="topics", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="topics", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject
    
class Post(models.Model):

    message = models.CharField(max_length=4000, null=True)
    topic = models.ForeignKey(Topic, related_name="posts", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        truncatord_message = Truncator(self.message)
        return truncatord_message.chars(30)

    





