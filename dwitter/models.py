

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    dob=models.DateField(blank=True,null=True)
    bio=models.CharField(max_length=50)
    profile_pic= models.ImageField(upload_to='static/profile_pic/userprofilepic/',null=True,blank=True)
    is_online=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        #Profile.objects.create(user=instance)
        user_profile=Profile(user=instance) 
        user_profile.save()
        print("success")
        user_profile.follows.add(user_profile)
        user_profile.save()
        
class Dweet(models.Model):
    user = models.ForeignKey(
        User, related_name="dweets", on_delete=models.DO_NOTHING
    )
    title= models.CharField(max_length=100)
    post= models.ImageField(upload_to='static/post/',null=True,blank=True)
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    likedby = models.ManyToManyField(User,related_name="likes",blank=True)
    
    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )


class Comment(models.Model):
    dweet=models.ForeignKey(Dweet,related_name="comments",on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="comments", on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )