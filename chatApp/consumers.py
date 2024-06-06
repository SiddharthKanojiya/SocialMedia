import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from chatApp.models import Mychats,Mygroup,Mygroupchats
from django.contrib.auth.models import User
from time import sleep
import datetime
from channels.db import database_sync_to_async



class MychatApp(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("connecting to 1 to 1.......")
        
        #print(type(self.scope['url_route']['kwargs']['room_name']),self.scope['url_route']['kwargs']['room_name'])
        await self.accept()
        #print(self.scope,self.scope['url_route']['kwargs'])
        if self.scope['url_route']['kwargs']:
            print("this")
            print(self.scope['url_route']['kwargs'])
            string=self.scope['url_route']['kwargs']['room_name']
            #string=string.replace('%20',' ')
            print(string,self.scope)
            roomname=string
            
        else:
            roomname=self.scope['user']
        roomname=f"mychat_app_{roomname}"
        await self.channel_layer.group_add(roomname, self.channel_name)
        
    async def receive(self, text_data):
        text_data = json.loads(text_data)
        print("receiving")
        #print("yjis",type(text_data['group']))
        if 'group' in text_data:
            roomname=text_data['group']
        else:
            roomname=text_data['user']
        await self.channel_layer.group_send(
            f"mychat_app_{roomname}",
            {
                'type':'send.msg',
                'msg':text_data['msg'],
                'curruser':text_data['curruser'],
                
            }
            )
        print(text_data)
        await self.save_chat(text_data)
        print("done")
    
    @database_sync_to_async   
    def save_chat(self,text_data):
        if 'group' in text_data:
            group=Mygroup.objects.get(name=text_data['group'])
            mychats, created = Mygroupchats.objects.get_or_create(group=group)
            # If the object was just created, initialize the 'chats' field as an empty dictionary
            if created:
                mychats.chats = {}
            user=self.scope['user']
            mychats.chats[str(datetime.datetime.now())+"1"] = {'user':user.username , 'msg': text_data['msg'],}
            mychats.save()
        else:
            
            frnd = User.objects.get(username=text_data['user'])
            mychats, created = Mychats.objects.get_or_create(me=self.scope['user'], frnd=frnd)
            # If the object was just created, initialize the 'chats' field as an empty dictionary
            if created:
                mychats.chats = {}
            mychats.chats[str(datetime.datetime.now())+"1"] = {'user': 'me', 'msg': text_data['msg']}
            mychats.save()
            mychats, created = Mychats.objects.get_or_create(me=frnd, frnd=self.scope['user'])
            # If the object was just created, initialize the 'chats' field as an empty dictionary
            if created:
                mychats.chats = {}
            mychats.chats[str(datetime.datetime.now())+"2"] = {'user': frnd.username, 'msg': text_data['msg']}
            mychats.save ()
        
        
        
        
        
    """ @database_sync_to_async   
    def save_chat(self,text_data):
        #frnd = User.objects.get(username=text_data['user'])
        group=Mygroup.objects.get(name=text_data['group'])
        mychats, created = Mygroupchats.objects.get_or_create(group=group)
        # If the object was just created, initialize the 'chats' field as an empty dictionary
        if created:
            mychats.chats = {}
        user=self.scope['user']
        mychats.chats[str(datetime.datetime.now())+"1"] = {'user':user.username , 'msg': text_data['msg'],}
        mychats.save()"""
        
    
    async def disconnect(self,closecode):
        print("terminating")
        pass
    
    async def send_msg(self,event):
        #print("---------",event['user'],self.scope['user'])
        print("888",self.scope['user'].username)
        #print(self.scope['user'].username,event['user'])
        if event['curruser']!=self.scope['user'].username:
            
            await  self.send(event['msg'])