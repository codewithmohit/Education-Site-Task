from django.shortcuts import render,redirect
from django.http import Http404
from .models import Ncert,Profile
from math import ceil
from  youtube_search  import  YoutubeSearch 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import transaction,DatabaseError
from datetime import date
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    videos=Ncert.objects.all()
    allVideos=[]
    n = len(videos)
    nSlides = n // 3 + ceil((n / 3) - (n // 3))
    allVideos.append([videos, range(1, nSlides), nSlides])
    params={'allVideos':allVideos}
    # import pdb;
    # pdb.set_trace()
    return render(request,'home.html',params)

def signup(request):
    if request.method=='POST':
        f_name=request.POST['fname']
        l_name=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        phone=request.POST['phone']
        gender=request.POST['gender']
        today=date.today()
        
        try:
            with transaction.atomic():
                user=User.objects.create_user(username=email,first_name=f_name,last_name=l_name,password=password,email=email,date_joined=today)
                profile=Profile.objects.create(user=user,phone=phone,gender=gender)
                user.save()
                profile.save()
                return redirect('login')
        except DatabaseError:
             # The transaction has failed. Handle appropriately
             raise Http404("Something is wrong")
    return render(request,'signup.html')

def handleLogin(request):
    if request.method=='POST':
        loginUsername=request.POST.get('email')
        loginPassword=request.POST.get('password')
        user=authenticate(username=loginUsername,password=loginPassword)
        if user is not None:
            login(request,user)
            profile=Profile.objects.get(user=request.user)
            print(profile)
            return redirect('/')

        else:
            print("++++")
            return redirect('login')
    return render(request,'login.html')

def handleLogout(request):
    logout(request)
    return redirect("/")

def search_videos(query):
    f_result={}
    result=YoutubeSearch(query, max_results=9).to_dict()
   
    for i in result:
        views=i['views']
        id=i['id']
        if views!=0:
            l=views.split()
            s=l[0]
            view=s.replace(",","")
            f_result[id]=int(view)
            
        else:
            f_result[id]=int(views)
    
    f_result = sorted(f_result, key=f_result.get,reverse=True)  

    return f_result


def search(request):
    query = request.GET.get('search')
    result=search_videos(query)
    params={'result':result,'search':query}
    return render(request, "search_video.html", params)