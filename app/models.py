from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe

class User(AbstractUser):

    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    TYPE = (
        ('student','Student'),
        ('teacher','Teacher'),
    )

    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(_('email address'), unique = True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)
    profile = models.ImageField(upload_to='users/profile', max_length=254, default='/users/profile/user-profile.png')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username' ,'first_name', 'last_name']
    
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def img_preview(self):
        return mark_safe(f'<img src = "{self.profile.url}" width = "300"/>')
    
    def __str__(self):
        return "{}".format(self.name)

class Post(models.Model):
   
    PUBLISH_TYPE = (
        ('public', 'Public'),
        ('private', 'Private'),
    )
    title = models.CharField(max_length=100, unique=True)
    publish = models.CharField(max_length=50, choices=PUBLISH_TYPE, default='public')
    description = models.TextField(max_length=1000)
    content = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='blog/', max_length=254, default='/blog/Default.png')
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_soft_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.title} - {self.user.name}'
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    is_soft_deleted = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.post.title} - {self.user.username}'

    class Meta:
        unique_together = ('post', 'user')