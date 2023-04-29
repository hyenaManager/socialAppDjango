from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import *

# Create your views here.

def home(request):
    if request.method == 'POST':
        # print(int(request.POST['post_id']))
        pk = int(request.POST['post_id'])
        postL = Post.objects.get(id=pk)
        like = Like.objects.filter(user=request.user,post=postL)
        # print('ajax pass this section')
        if like:
            like.delete()
            postL.like_decrement()
            like.noti = str(request.user.username)+' unlike your post'
        else:
            Like.objects.create(
            user = request.user,post=postL,
            noti = str(request.user.username)+' like your post',
            postOwner = postL.user)
            postL.like_increment()
        return JsonResponse({'success': True, 'like_count': postL.like_count})
    print("if section end!")
    posts = Post.objects.all()
    pP = UserProfile.objects.get(user = request.user.id)
    likeNoti = Like.objects.filter(postOwner = request.user.username)
    context = {
        'user_name': request.user,
        'posts': posts,
        'userP': pP,
        'notifications': likeNoti,
        'post': posts, # pass the first post object to the context
    }
    return render(request,'home.html',context)

def view_post(request,pk):
    get_post = Like.objects.get(id=pk)
    get_postId = get_post.post.id
    viewPost = Post.objects.get(id=get_postId)
    posts = Post.objects.all()
    pP = UserProfile.objects.get(user = request.user.id)
    likeNoti = Like.objects.filter(postOwner = request.user.username)
    context = {
        'user_name': request.user,
        'posts': posts,
        'view_post':viewPost,
        'userP': pP,
        'notifications': likeNoti,
        'post': posts, # pass the first post object to the context
    }
    return render(request,'home.html',context)



@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user.save()
            UserProfile.objects.create(user = user)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        userP = UserProfile.objects.get(user = request.user)
        post = Post.objects.create(
            user = request.user,
            user_profile = userP,
            title=title,
            content=content,
            # user_id = request.user.id its only used when we do not set the foreignkey
            )
        post.save()
        return redirect('home')
    return render(request,'create_post.html',{'user_name':request.user.username})

def create_userPp(request):
    if request.method == 'POST':
        profile_pict = request.FILES.get('profile_picture')
        userBio = request.POST['bio']
        userP = UserProfile.objects.get(user=request.user.id)
        if request.FILES.get('profile_picture') != None:
            userP.profile_pic = profile_pict
        userP.bio = userBio
        userP.save()
        return redirect('home')
    userP = UserProfile.objects.get(user=request.user.id)
    return render(request,'userProfile.html',{
        "user_profile":userP
    })
def like(request,pk):
    if request.method == 'POST':
        pk = request.POST['post_id']
        post = Post.objects.get(id=pk)
        like = Like.objects.filter(user=request.user,post=post).first()
        if like:
            like.delete()
            post.like_decrement()
            like.noti = str(request.user.username)+' unlike your post'
        else:
            Like.objects.create(
                user = request.user,post=post,
                noti = str(request.user.username)+' like your post',
                postOwner = post.user)
            post.like_increment()

    return redirect('home')

def notification(request):
    pass