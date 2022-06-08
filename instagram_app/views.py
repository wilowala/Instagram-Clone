from django.shortcuts import render, redirect, get_object_or_404
from multiprocessing import context
from django.contrib.auth import authenticate, login as authlogin,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect

from .forms import RegisterForm, AddImageForm, UpdateImageForm, UpdateProfileForm
from .emails import send_welcome_email
from instagram_app.models import Image, Profile, Follow, Comment, Likes

# Create your views here.
def login(request):
    try:
        page = 'login'
        if request.method == 'POST':
            username = request.POST.get('username').lower()
            password = request.POST.get('password')

            try:
                user = User.objects.get(username=username)
            except Exception as e:
                messages.error(request, 'User does not exist')
                print(e)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                authlogin(request, user)
                return redirect('home')
            else:
                messages.error(request, 'username or password does not exist')
        context = {'page': page}
        return render(request, 'instagram_app/login.html', context)
    except:
        HttpResponse(request, 'Not working!')

def register(request):
    form = RegisterForm()
    page = 'register'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            recipient = User(username=username, email=email)
            send_welcome_email(username, email)

            profile = Profile.objects.create(name=username, owner=user)
            profile.save()
        return redirect(request, 'instagram_app/login.html',)
    context = {'page': page, 
               'form': form,}
    return render(request, 'instagram_app/register.html', context)

def logout(request):
    # logout(request)
    return redirect('login')

@login_required(login_url='')
def home(request,):
    images = Image.objects.all()
    profile = request.user
    print(profile)
    profile_info = Profile.objects.get(owner=profile)
    # profile_info=Profile.objects.filter(owner=profile.id)[0]

    profiles = Profile.objects.all()

    context = {'images': images, 
               'profile_info': profile_info, 
               'profiles':profiles}
    return render(request, 'instagram_app/index.html', context)

@login_required(login_url='')
def search(request):
    query = request.GET.get('q')
    if query:
        images = Image.objects.filter(
            Q(image_name__icontains=query) |
            Q(owner__name__icontains=query) |
            Q(image_caption__icontains=query)
        )
        context = {'images': images}
        return render(request, 'instagram_app/search.html', context)


@login_required(login_url='')
def upload_images(request):
    form = AddImageForm()
    user = request.user
    owner = Profile.objects.get(owner=user)
    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_name = form.cleaned_data['image_name']
            image_caption = form.cleaned_data['image_caption']
            upload = Image(image=image, image_name=image_name,
                           image_caption=image_caption, owner=owner)
            upload.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'instagram_app/upload.html', context)


@login_required(login_url='')
def delete_image(request, pk):
    image = Image.objects.get(id=pk)
    if request.method == "POST":
        image.delete()
        return redirect('home')
    return render(request, 'instagram_app/delete.html', {'obj': image})


@login_required(login_url='')
def update_image(request, pk):
    image = Image.objects.get(id=pk)
    form = UpdateImageForm(request.POST or None, instance=image)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.owner = request.user.profile
            form.instance.image = image.image
            form.instance.image_name = image.image_name
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'instagram_app/update.html', context)


@login_required(login_url='')
def comments(request, pk):
    image = Image.objects.get(id=pk)
    comments = Comment.objects.filter(image=image)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        print(comment)
        comment_owner = Profile.objects.get(owner=request.user)
        new_comment = Comment.objects.create(
            comment=comment, image=image, owner=comment_owner)
        new_comment.save()

    context = {'comment': comments, 'image': image}
    return render(request, 'instagram_app/comments.html', context)


@login_required(login_url='')
def profiles(request):
    user = request.user
    profile = Profile.objects.get(owner=user)

    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()

    images = Image.objects.filter(owner=profile)
    context = {'profile': profile, 'images': images, 'following_count':following_count,'followers_count':followers_count,}
    return render(request, 'instagram_app/profile.html', context)


def update_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    form = UpdateProfileForm(request.POST, instance=profile)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {'form': form}
    return render(request, 'instagram_app/update.html', context)


def like(request, pk):
    user = request.user
    image = Image.objects.get(id=pk)
    current_likes = image.likes
    liked = Likes.objects.filter(user=user, image=image).count()

    if not liked:
            class_name = 'red'
            like = Likes.objects.create(user=user, image=image)
            current_likes = current_likes + 1

    else:
            Likes.objects.filter(user=user, image=image).delete()
            current_likes = current_likes - 1

    image.likes = current_likes
    image.save()

    return HttpResponseRedirect(reverse('home'))


def unfollow(request, pk):
    if request.method == 'GET':
        try:
            user_profile2 = User.objects.get(username=pk)
        except User.DoesNotExist:
            user_profile2 = None

        unfollow_d = Follow.objects.filter(follower=request.user, following=user_profile2)
        unfollow_d.delete()
        return redirect('profile')

def follow(request, pk):
    if request.method == 'GET':
        try:
            user_profile3 = User.objects.get(username=pk)
        except User.DoesNotExist:
            user_profile3 = None

        follow_s = Follow(follower=request.user, following=user_profile3)
        follow_s.save()
        return redirect('profile')