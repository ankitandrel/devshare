from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    category_name_slug = models.SlugField(max_length=50, unique=True)
    category_info = models.CharField(max_length=500, default=None, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'

    def get_url(self):
         return reverse('resource_by_category', args=[self.category_name_slug])


class Resource(models.Model):
    resource_name = models.CharField(max_length=200)
    resource_slug = models.SlugField(max_length=200, unique=True)
    resource_category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    resource_link = models.URLField(max_length=10000, unique=True)
    resource_info = models.TextField()
    resource_posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.ManyToManyField(User, blank=True, related_name='likes')
    is_featured = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    on_homepage = models.BooleanField(default=False)
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.resource_name

    def numbmer_of_likes(self):
        return self.liked.count()

    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resource'

    


class Article(models.Model):
    article_title =  models.CharField(max_length=500)
    article_link = models.URLField(max_length=5000, unique=True)
    article_info = models.TextField(blank=True, default="No information provided about this article")
    article_tag = TaggableManager()
    liked = models.ManyToManyField(User, blank=True, related_name='like')
    is_featured = models.BooleanField(default=False)
    article_posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    article_posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article_title
    def numbmer_of_likes(self):
        return self.liked.count()


class Like_Unlike(models.Model): 

    choice = (
        ('Like', 'Like'),
        ('Unlike', 'Unlike'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, blank=True,null=True)
    article = models.ForeignKey(Article,on_delete=models.CASCADE, blank=True,null=True)
    value = models.CharField(choices=choice, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}-Resource: {self.resource} Article: {self.article} Value-{self.value}"

