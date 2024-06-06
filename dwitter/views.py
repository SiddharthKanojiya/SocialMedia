# dwitter/views.py

from django.shortcuts import render,redirect
from .models import Profile,Dweet,Comment
from django.contrib.auth.decorators import login_required
from . import forms,models
from django.http import HttpResponseRedirect,HttpResponse
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.contrib.auth.models import User


@receiver(user_logged_in)
def got_online(sender,user,request,**kwargs):
    print(user)
    """user.profile.is_online = True
    user.save()"""
    curruser=Profile.objects.get(user=user)
    curruser.is_online=True
    curruser.save()
    
    print("HEllo",user.profile.is_online,user.username,curruser.is_online)

@receiver(user_logged_out)
def got_offline(sender,user,request,**kwargs):
    curruser=Profile.objects.get(user=user)
    curruser.is_online=False
    curruser.save()
    print("bye")
    print("bye",user.profile.is_online,user.username,curruser.is_online)
    

def signup(request):
    profiles=Profile.objects.all()
    usernames=[x.user.username for x in profiles]
    
    userForm=forms.SignUpForm()
    profileForm=forms.ProfileForm()
    mydict={'userForm':userForm,'profileForm':profileForm,'usernames':usernames}
    if request.method=='POST':
        print("post")
        userForm=forms.SignUpForm(request.POST)
        profileForm=forms.ProfileForm(request.POST,request.FILES)
        if userForm.is_valid() and profileForm.is_valid():
            
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            user_profile=Profile.objects.get(user=user)
            print(user_profile)
            print(profileForm.cleaned_data['dob'])
            user_profile.dob=profileForm.cleaned_data['dob']
            user_profile.bio=profileForm.cleaned_data['bio']
            user_profile.profile_pic=profileForm.cleaned_data['profile_pic']
            
            user_profile.save()
            """customer=profileForm.save(commit=False)
            customer.user=user
            customer.save()"""
        else:
            mydict['msg']="A user with that username already exist"
            return render(request,'dwitter/signup.html',context=mydict)

            
    
        return HttpResponseRedirect('userlogin')
    return render(request,'dwitter/signup.html',context=mydict)

def userlogin(request):
    print(request.user)
    return render(request, "dwitter/userlogin.html")
def afterlogin_view(request):
    """curruser=Profile.objects.get(user=request.user)
    curruser.is_online=True
    curruser.save()"""
    return redirect('dashboard')
@login_required()
def dashboard(request):
    if request.method == "POST":
        data = request.POST
        action = data.get("likebtn")
        print(action)
        if action!=None:
            arr=action.split('-')
            did=arr[0]
            act=arr[1]
            dweet=Dweet.objects.get(id=did)
            if act == "like":
                dweet.likedby.add(request.user)
            elif act == "unlike":
                dweet.likedby.remove(request.user)
            dweet.save()
        # create a form instance and populate it with data from the request:
        form = forms.CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            #user_profile=Dweet.objects.get(pk=pk)
            #print(user_profile)
            #print("hello")
            #print(Dweet.objects.get(pk=form.cleaned_data['dweetid']))
            comment=Comment.objects.create(dweet=Dweet.objects.get(pk=form.cleaned_data['dweetid']),user=request.user,body=form.cleaned_data['body'])
            #print(form.cleaned_data['body'])
            comment.save()
            # redirect to a new URL:
            return HttpResponseRedirect("dashboard")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.CommentForm()
    print(request.user)
    profiles=Profile.objects.all()
    mails=[x.user.email for x in profiles]
    
    dct={"mails":mails,"form":form}
    return render(request, "dwitter/dashboard.html",context=dct)
@login_required()
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})

def base(request):
    if request.user.is_authenticated:
        HttpResponseRedirect('dwitter/dashboard')
    return render(request,"base.html")
@login_required()
def profile(request, pk):
    """below section has to deleted"""
    """if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()"""

    
    
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    print(profile.is_online,profile.user.username,request.user.username,request.user.profile.is_online)
    return render(request, "dwitter/profile.html", {"profile": profile})

@login_required()
def adddweet(request):
    dweetForm=forms.DweetForm()
    if request.method=='POST':
        dweetForm=forms.DweetForm(request.POST, request.FILES)
        if dweetForm.is_valid():
            dweet=dweetForm.save(commit=False)
            dweet.user=request.user
            dweet.save()
            #dweetForm.save()
            """dweet=Dweet.objects.get(body=dweetForm.cleaned_data['body'])
            print(dweet)
            dweet.user=request.user
            dweet.save()"""
        return HttpResponseRedirect('dashboard')
    
    return render(request, "dwitter/dweet.html",{'dweetForm':dweetForm})


@login_required()
def addComment(request,pk):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = forms.CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            #user_profile=Dweet.objects.get(pk=pk)
            #print(user_profile)
            comment=Comment.objects.create(dweet=pk,user=request.user,body=form.cleaned_data['body'])
            print(form.cleaned_data['body'])
            comment.save()
            # redirect to a new URL:
            return HttpResponseRedirect("dashboard")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.CommentForm()

    return render(request, "dashboard.html", {"form": form})