from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MyUser(models.Model):
    user_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self) -> str:
        return self.user_name
    
    class Meta:
        ordering = ['user_name']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200,default='user does not provied bio')
    location = models.CharField(max_length=200,blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/',default="sample_ajax/ajaxTest/static/images/default_user.jpg")
    interests = models.CharField(max_length=200,blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True,default='no twitter')
    facebook_handle = models.CharField(max_length=50, blank=True,default='no facebook')
    instagram_handle = models.CharField(max_length=50, blank=True,default='no instagram')

    class Meta:
        ordering = ['user']

    def userName(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(default="sample_ajax/ajaxTest/static/images/default_user.jpg")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    like_count = models.PositiveIntegerField(default=0)

    # def userProfile(self):
    #     return self.user.profile_pic
    
    def userName(self):
        return self.user.user
    
    def like_increment(self):
        self.like_count +=1
        self.save()

    def like_decrement(self):
        self.like_count -=1
        self.save()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    noti = models.TextField(default='someone like your post')
    postOwner = models.CharField(max_length=100)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

