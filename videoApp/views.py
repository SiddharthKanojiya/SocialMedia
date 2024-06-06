from django.shortcuts import render
from django.http import JsonResponse
import random

import time
from agora_token_builder import RtcTokenBuilder

#from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Create your views here.
@login_required
def lobby(request):
    return render(request, 'videoApp/lobby.html')
@login_required
def room(request):
    return render(request, 'videoApp/room.html')
@login_required
def getToken(request):
    appId=os.environ.get('APP_ID')
    appCertificate=os.environ.get('APPCERTIFICATE')
    #appId = "b7b54b5a22524682926b05e18e040455"
    #appCertificate = "075d69c5ffd54c438a102806cbbd4ed5"
    channelName = request.GET.get('channel')
    print(request.user.id)
    uid = request.user.id
    users=User.objects.all()
    userstr=""
    uidstr=""
    for user in users:
        userstr+=user.username+" "
        uidstr+=str(user.id)+" "
        
    print(userstr)
    print(uidstr)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid,'userstr':userstr,'uidstr':uidstr,'appid':appId}, safe=False)
