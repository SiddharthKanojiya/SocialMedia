from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Mychats(models.Model):
    me = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='it_me')
    frnd = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='my_frnd')
    chats = models.JSONField(default=dict)

class Mygroup(models.Model):
    name=models.CharField(max_length=30)
    member=models.ManyToManyField(User,related_name='mygroup')
    
    def __str__(self):
        return self.name
    #chats = models.JSONField(default=dict)
class Mygroupchats(models.Model):
    #gpmember = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='it_mee')
    group = models.ForeignKey(to=Mygroup,on_delete=models.CASCADE,related_name='groupchat')
    chats = models.JSONField(default=dict)