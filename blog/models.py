from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from datetime import datetime

def validate_file_exceptions(value):
    import os 
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extention = ['.jpj', '.png']
    if not ext.lower() in valid_extention:
        raise ValidationError('unsupported file extension!')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='files/user_avatar', null=False, blank=False, validators=[validate_file_exceptions])
    description = models.CharField(max_length=512, null=False, blank=False)


class Article(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    cover = models.FileField(upload_to='files/artivle_cover/', null=False, blank=False, validators=[validate_file_exceptions])
    content = RichTextField()
    created_at = models.DateTimeField(default=datetime.now, blank=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    author = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

class Category(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    cover = models.FileField(upload_to='files/category_cover', null=False, blank=False, validators=[validate_file_exceptions])
