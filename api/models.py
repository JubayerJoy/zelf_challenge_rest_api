from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator
from django.db import models

class Author(models.Model):
    unique_id = models.IntegerField(unique=True, validators=[MinValueValidator(0), MaxValueValidator(2147483647)])
    unique_uuid = models.CharField(max_length=100)
    origin_unique_id = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    platform = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    followers_count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2147483647)])
    avatar_url = models.URLField()
    profile_text = models.TextField()

class Content(models.Model):
    unique_id = models.IntegerField(unique=True, validators=[MinValueValidator(0), MaxValueValidator(2147483647)])
    unique_uuid = models.CharField(max_length=100)
    origin_unique_id = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    main_text = models.TextField()
    token_count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2147483647)])
    char_count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2147483647)])
    tag_count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2147483647)])
    origin_platform = models.CharField(max_length=50)
    origin_url = models.URLField()
    media_url = models.URLField()
    media_type = models.CharField(max_length=50)
    likes_count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2147483647)])
    views_count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2147483647)])
    comments_count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2147483647)]) 