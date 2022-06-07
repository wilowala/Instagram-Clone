from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    profile_photo = models.ImageField(upload_to='profile/', default='profile/default.png')
    bio = models.CharField(max_length=300)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return self.name

class Image(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField( upload_to='photos/', height_field=None, width_field=None, max_length=100)
    image_name = models.CharField(max_length=200)
    image_caption = models.TextField(blank=True)
    likes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
            return self.image_name
    
    def number_of_likes(self):
        return self.likes.count()

    def save_image(self):
        return self.save()

    def delete_image(self):
        return self.delete()

    def update_caption(self, pk):
        image_caption =self.objects.get(image_caption=pk)
        return image_caption.save()

    class Meta:
        ordering = ['-created']

class Comment(models.Model):
    comment = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
            return self.comment

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='post_like')

    def user_liked_post(sender, instance, *args, **kwargs):
            like = instance
            post = like.post
            sender = like.user

    def user_unlike_post(sender, instance, *args, **kwargs):
            like = instance
            post = like.post
            sender = like.user

class Follow(models.Model):
        follower = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='follower')
        following = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='following')

        def user_follow(sender, instance, *args, **kwargs):
            follow = instance
            sender = follow.follower
            following = follow.following

        def user_unfollow(sender, instance, *args, **kwargs):
            follow = instance
            sender = follow.follower
            following = follow.following