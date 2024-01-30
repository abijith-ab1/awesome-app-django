from django.shortcuts import render, redirect, get_object_or_404
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
                    
                post.save()
                form.save_m2m()
                return redirect('/')
            
            except Exception as e:
                print('Error:', e)
                
    return render(request, 'a_posts/post_create.html', {'form': form})

def post_delete_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully...")
        return redirect('/')
    return render(request, 'a_posts/post_delete.html', {'post': post})

def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk)
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
    return render(request, 'a_posts/post_page.html', {'post': post})