from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime


User = get_user_model()

# Create your models here.
class Profile(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 id_user = models.IntegerField()
 bio = models.TextField(blank=True) 
 profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png') 
 backimg = models.ImageField(upload_to='background_images', default='timeline-1.jpg') 
 location = models.CharField(max_length=100, blank=True)

 def __str__(self):
  return self.user.username


class Post(models.Model):
 id = models.UUIDField(primary_key=True, default=uuid.uuid4)
 user = models.CharField(max_length=100)
 image = models.FileField(upload_to='post_attachments',blank=True, null=True)
 pfp = models.ImageField(upload_to='post_images', default='blank-profile-picture.png')
 caption = models.TextField()
 created_at = models.DateTimeField(default=datetime.now)
 no_of_likes = models.IntegerField(default=0)
 no_of_comments = models.IntegerField(default=0)
 comments_enabled = models.BooleanField(default=True)

 def __str__(self):
  return self.user


class LikePost(models.Model):
 post_id = models.CharField(max_length=500)
 username = models.CharField(max_length=100)

 def __str__(self):
  return self.username


class FollowersCount(models.Model):
 follower = models.CharField(max_length=100)
 user = models.CharField(max_length=100)

 def __str__(self):
  return self.user


class Comment(models.Model):
 post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
 name = models.CharField(max_length=80)
 email = models.EmailField()
 body = models.TextField()
 created_on = models.DateTimeField(auto_now_add=True)
 active = models.BooleanField(default=False)

 class Meta:
  ordering = ['created_on']

 def __str__(self):
  return 'Comment {} by {}'.format(self.body, self.name)


# class Notification(models.Model):
#  to = models.ForeignKey(User, on_delete=models.CASCADE)
#  sent_from = models.CharField(max_length=100, blank=True, null=True)
#  timestamp = models.DateTimeField(auto_now_add=True)
#  message = models.TextField()
#  is_read = models.BooleanField(default=False)

#  def __str__(self):
#   return self.to


class Favorite(models.Model):
 post = models.ForeignKey(Post, on_delete=models.CASCADE)
 user = models.CharField(max_length=100)
 time = models.DateTimeField(auto_now_add=True)

 def __str__(self):
  return self.user