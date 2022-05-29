from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    name_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='user')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    updated = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.content} by {self.name}"


class CwUsers(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='cw_user')
    cw_name = models.CharField(max_length=80)
    cw_id = models.IntegerField()
