from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from bs4 import BeautifulSoup
import requests
import urllib.request
from urllib.request import urlopen

from .models import *
from .forms import *

def home_view(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()
    
    categories = Tag.objects.all()
    
    context = {
        'posts': posts,
        'categories': categories,
        'tag': tag
    }
    return render(request, 'a_posts/home.html', context)
@login_required
def post_create_view(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            
            try:
                website = urllib.request.urlopen(form.data['url'])
                sourcecode = BeautifulSoup(website, 'html.parser')
                
                find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
                if find_image:
                    image = find_image[0]['content']
                    post.image = image
                
                find_title = sourcecode.select('h1.photo-title')
                if find_title:
                    title = find_title[0].text.strip()
                    post.title = title
                
                find_artist = sourcecode.select('a.owner-name')
                if find_artist:
                    artist = find_artist[0].text.strip()
                    post.artist = artist
                
                post.author = request.user
                    
                post.save()
                form.save_m2m()
                return redirect('/')
            
            except Exception as e:
                print('Error:', e)
                
    return render(request, 'a_posts/post_create.html', {'form': form})
@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully...")
        return redirect('/')
    return render(request, 'a_posts/post_delete.html', {'post': post})

@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    form = PostEditForm(instance=post)
    
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post you edited successfully...')
            return redirect('/')
    else:
        form = PostEditForm(instance=post)
    
    context = {
        'post': post,
        'form' : form
    }   
    return render(request, 'a_posts/post_edit.html', context)

def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()

    context = {
        'post': post,
        'commentform': commentform,
        'replyform': replyform
    }
    
    return render(request, 'a_posts/post_page.html', context)

@login_required
def comment_sent(request, pk):
    post =  get_object_or_404(Post, id=pk)
    
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
    return redirect('post', post.id)

@login_required
def comment_delete_view(request, pk):
    post = get_object_or_404(Comment, id=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Comment deleted successfully...")
        return redirect('post', post.parent_post.id)
    
    return render(request, 'a_posts/comment_delete.html', {'comment': post})

@login_required
def reply_sent(request, pk):
    comment =  get_object_or_404(Comment, id=pk)
    
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()
            
    return redirect('post', comment.parent_post.id)


@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)
    
    if request.method == 'POST':
        reply.delete()
        messages.success(request, "Reply deleted successfully...")
        return redirect('post', reply.parent_comment.parent_post.id)
    
    return render(request, 'a_posts/reply_delete.html', {'reply': reply})

def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    user_exists = post.likes.filter(username=request.user.username).exists()
    
    if post.author != request.user:
        if user_exists:
            post.likes.remove(request.user)
        else:  
            post.likes.add(request.user)
    
    return render(request, 'snippets/likes.html', {'post': post})