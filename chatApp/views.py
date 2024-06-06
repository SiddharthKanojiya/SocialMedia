from django.shortcuts import render
from chatApp.models import Mychats,Mygroupchats,Mygroup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dwitter.models import Profile
from chatApp.forms import GroupForm
from django.http import HttpResponseRedirect
# Create your views here.

@login_required
def chating(request):
    frnd_name = request.GET.get('user',None)
    mychats_data = None
    if frnd_name:
        if User.objects.filter(username=frnd_name).exists() and Mychats.objects.filter(me=request.user,frnd=User.objects.get(username=frnd_name)).exists():
            frnd_ = User.objects.get(username=frnd_name)
            mychats_data = Mychats.objects.get(me=request.user,frnd=frnd_).chats
    frndprofile=request.user.profile.follows.exclude(user=request.user)
    followerprofile=Profile.objects.exclude(id__in =frndprofile).exclude(user=request.user)

    print(followerprofile)
    print(frndprofile)
    frnds = User.objects.exclude(pk=request.user.id)
    return render(request,'chatApp/chating.html',{'my':mychats_data,'chats': mychats_data,'frnds':frnds,'frndprofile':frndprofile,'followerprofile':followerprofile})


@login_required
def group_chat(request):
    gp = request.GET.get('gp',None)

    mygroupchats_data = None
    members=None
    if gp:
        if Mygroup.objects.filter(name=gp).exists() and Mygroupchats.objects.filter(group=Mygroup.objects.get(name=gp)).exists():
            mygroup = Mygroup.objects.get(name=gp)
            allc=Mygroupchats.objects.all()
            #print(allc)
            mygroupchats_data=Mygroupchats.objects.get(group=mygroup).chats
            members=mygroup.member.all()
            #print(mygroupchats_data)
            
    
    #frnds = User.objects.exclude(pk=request.user.id)
    groups=Mygroup.objects.all()
    
    return render(request,'chatApp/group_chat.html',{'groups':groups,'chats': mygroupchats_data,'members':members})



def createGroup(request):
    users=User.objects.all()
    
    usernames=[x.username for x in users]
    
    groupForm=GroupForm()
    
    mydict={'groupForm':groupForm,'usernames':usernames}
    if request.method=='POST':
        print("post")
        groupForm=GroupForm(request.POST)
        
        if groupForm.is_valid() :
            
            user=groupForm.save()
            name=groupForm.cleaned_data['name']
            user.save()
            group=Mygroup.objects.get(name=name)
            group.name=name.replace(' ','_')
            group.save()
    
            #print(profileForm.cleaned_data['profile_pic'])
            """customer=profileForm.save(commit=False)
            customer.user=user
            customer.save()"""
        else:
            mydict['msg']="A user with that username already exist"
            return render(request,'chatApp/creategroup.html',context=mydict)

            
    
        #return HttpResponseRedirect('group_chat')
    return render(request,'chatApp/creategroup.html',context=mydict)