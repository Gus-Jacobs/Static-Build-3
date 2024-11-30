from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount, Comment, Favorite
from itertools import chain
import random
import os
import sys

# Create your views here.

@login_required(login_url='signin')
def index(request):
 user_object = User.objects.get(username=request.user.username)
 user_profile = Profile.objects.get(user=user_object)

 user_following_list = []
 feed = []

 user_following = FollowersCount.objects.filter(follower=request.user.username)

 for users in user_following:
  user_following_list.append(users.user)

 for usernames in user_following_list:
  feed_lists = Post.objects.filter(user=usernames)
  feed.append(feed_lists)

 feed_list = list(chain(*feed))
 posts = Post.objects.all()


 all_users = User.objects.all()
 user_following_all = []

 for user in user_following:
  user_list = User.objects.get(username=user.user)
  user_following_all.append(user_list)

 new_suggestion_list = [x for x in list(all_users) if(x not in list(user_following_all))]
 current_user = User.objects.filter(username=request.user.username)
 final_suggestion_list = [x for x in list(new_suggestion_list) if(x not in list(current_user))]
 random.shuffle(final_suggestion_list)

 username_profile = []
 username_profile_list = []

 for users in final_suggestion_list:
  username_profile.append(users.id)
 for ids in username_profile:
  profile_lists = Profile.objects.filter(id_user=ids)
  username_profile_list.append(profile_lists)

 suggestions_username_profile_list = list(chain(*username_profile_list))


 favorites = Favorite.objects.filter(user=request.user.username)

 return render(request, 'index.html', {'user_profile': user_profile, 'posts': posts, 'suggestions_username_profile_list': suggestions_username_profile_list[:4], 'favorites': favorites})


@login_required(login_url='signin')
def upload(request):
 if request.method == 'POST':
  user = request.user.username
  image = request.FILES.get('image_upload')
  if image == None:
   messages.info(request, "No file selected")
   return redirect('/')
  if image.size > 6250000:
   messages.info(request, "File was too big! file size: {} MB | Maximum file size: {}".format(round(image.size/1024/1024), '50MB'))
   return redirect('/')
  caption = request.POST['caption']
  pfp = Profile.objects.get(user=request.user).profileimg
  formats = ['.JPG', '.PNG', '.GIF', '.MOV', '.MP4', '.MP3', '.M4A', '.JPEG']
  img_str = str(image)
  extension = os.path.splitext(img_str)[1]
  if extension.upper() in formats:
   new_post = Post.objects.create(user=user, image=image, caption=caption , pfp=pfp)
   new_post.save() 
   return redirect('/')

  else:
   messages.info(request, "File type not supported! Selected file type: {}".format(extension.upper()))
   return redirect('/')

 else:
  return render(request, 'index.html')


@login_required(login_url='signin')
def search(request):
 user_object = User.objects.get(username=request.user.username)
 user_profile = Profile.objects.get(user=user_object)
 if request.method == 'POST':
  username = request.POST['username']
  username_object = User.objects.filter(username__icontains=username)

  username_profile = []
  username_profile_list = []

  for users in username_object:
   username_profile.append(users.id)

  for ids in username_profile:
   profile_lists = Profile.objects.filter(user_id=ids)
   username_profile_list.append(profile_lists)

  username_profile_list = list(chain(*username_profile_list))

 return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})


@login_required(login_url='signin')
def like_post(request):
 username = request.user.username
 post_id = request.GET.get('post_id')

 post = Post.objects.get(id=post_id)
 like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

 if like_filter == None:
  new_like = LikePost.objects.create(post_id=post_id, username=username)
  new_like.save()

  post.no_of_likes = post.no_of_likes+1
  post.save()
  return redirect('/')
 else:
  like_filter.delete()
  post.no_of_likes = post.no_of_likes-1
  post.save()
  return redirect('/')


@login_required(login_url='signin')
def delete(request):
 post_id = request.GET.get('post_id')
 x = Post.objects.filter(id=post_id).first()
 os.remove('S:/Static build 3/Build 3.0/Static_B3'+x.image.url)
 print('worked')
 if Post.objects.filter(id=post_id).first():
  Post.objects.get(id=post_id).delete()
 return redirect('/')


@login_required(login_url='signin')
def disable_enable(request):
 post_id = request.GET.get('post_id')
 post = Post.objects.filter(id=post_id).first()
 if post.comments_enabled == False:
  Post.objects.filter(id=post_id).update(comments_enabled=True)
  return redirect('/')
 else:
  Post.objects.filter(id=post_id).update(comments_enabled=False)
  return redirect('/')



@login_required(login_url='signin')
def favorite(request):
 user = request.user.username
 post_id = request.GET.get('post_id')
 post = Post.objects.get(id=post_id)
 favorite_filter = Favorite.objects.filter(post=post, user=user).first()
 if favorite_filter == None:
  new_favorite = Favorite.objects.create(post=post, user=user)
  new_favorite.save()
  return redirect('/')
 else:
  favorite_filter.delete()
  return redirect('/')



@login_required(login_url='signin')
def comments(request):
 if request.method == 'POST':
  user = request.user.username
  message = request.POST['comment']
  post = Post.objects.filter(user=user).first()

  new_comment = Comment.objects.create(name=user, body=message, post=post)
  new_comment.save()
  return redirect('/')
 else:
  return redirect('/')



@login_required(login_url='signin')
def profile(request, pk):
 user_object = User.objects.get(username=pk)
 user_profile = Profile.objects.get(user=user_object)
 user_posts = Post.objects.filter(user=pk)
 user_post_length = len(user_posts)

 follower = request.user.username
 user = pk

 if FollowersCount.objects.filter(follower=follower, user=user).first():
  button_text = 'Unfollow'
 else:
  button_text = 'Follow'

 user_followers = len(FollowersCount.objects.filter(user=pk))
 user_following = len(FollowersCount.objects.filter(follower=pk))

 context = {'user_object': user_object, 'user_profile': user_profile,
  'user_posts': user_posts, 'user_post_length': user_post_length,
   'button_text': button_text, 'user_following': user_following,
   'user_followers': user_followers}
 return render(request, 'profile.html', context)


@login_required(login_url='signin')
def follow(request):
 if request.method == 'POST':
  follower = request.POST['follower']
  user = request.POST['user']

  if FollowersCount.objects.filter(follower=follower, user=user).first():
   delete_follower = FollowersCount.objects.get(follower=follower, user=user)
   delete_follower.delete()
   return redirect('/profile/'+user)
  else:
   new_follower = FollowersCount.objects.create(follower=follower, user=user)
   new_follower.save()
   return redirect('/profile/'+user)

 else:
  return redirect('/')


@login_required(login_url='signin')
def settings(request):
 user_profile = Profile.objects.get(user=request.user)

 if request.method == 'POST':
  if request.FILES.get('image') == None:
   image = user_profile.profileimg
   os.remove('S:/Static build 3/Build 3.0/Static_B3'+user_profile.backimg.url)
   bgi = request.FILES.get('bgi')
   bio = request.POST['bio']
   location = request.POST['location']

   user_profile.profileimg = image
   user_profile.backimg = bgi  
   user_profile.bio = bio 
   user_profile.location = location 
   user_profile.save()

  if request.FILES.get('bgi') == None:
   os.remove('S:/Static build 3/Build 3.0/Static_B3'+user_profile.profileimg.url)
   image = request.FILES.get('image')
   bgi = user_profile.backimg
   bio = request.POST['bio']
   location = request.POST['location']

   user_profile.profileimg = image
   user_profile.backimg = bgi  
   user_profile.bio = bio 
   user_profile.location = location 
   user_profile.save()

  if request.FILES.get('image') != None:
   os.remove('S:/Static build 3/Build 3.0/Static_B3'+user_profile.profileimg.url)
   image = request.FILES.get('image')
   bgi = user_profile.backimg
   bio = request.POST['bio']
   location = request.POST['location']

   user_profile.profileimg = image
   user_profile.backimg = bgi  
   user_profile.bio = bio 
   user_profile.location = location 
   user_profile.save()

  if request.FILES.get('bgi') != None:
   image = user_profile.profileimg
   os.remove('S:/Static build 3/Build 3.0/Static_B3'+user_profile.backimg.url)
   bgi = request.FILES.get('bgi')
   bio = request.POST['bio']
   location = request.POST['location']

   user_profile.profileimg = image
   user_profile.backimg = bgi  
   user_profile.bio = bio 
   user_profile.location = location 
   user_profile.save() 

  return redirect('settings')
 return render(request, 'setting.html', {'user_profile': user_profile})


def signup(request):

 if request.method == 'POST':
  username = request.POST['username']
  email = request.POST['email']
  password = request.POST['password']
  password2 = request.POST['password2']

  if password == password2:
   if User.objects.filter(email=email).exists():
    messages.info(request, "Selected Email Already in Use")
    return redirect('signup')
   elif User.objects.filter(username=username).exists():
    messages.info(request, "Selected Username Already Taken")
    return redirect('signup')   
   else:
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

    user_login = auth.authenticate(username=username, password=password)
    auth.login(request, user_login)


    user_model = User.objects.get(username=username)
    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
    new_profile.save()
    return redirect('settings')


  else:
   messages.info(request, "Passwords do not match")
   return redirect('signup')


 else:
  return render(request, 'signup.html')


def signin(request):

 if request.method == 'POST':
  username = request.POST['username']
  password = request.POST['password']

  user = auth.authenticate(username=username, password=password)

  if user is not None:
   auth.login(request, user)
   return redirect('/')
  else:
   messages.info(request, 'Credentials Invalid')
   return redirect('signin')

 else:
  return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
 auth.logout(request)
 return redirect('signin')
 # return render(request, '404.html')

