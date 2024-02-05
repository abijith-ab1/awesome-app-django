from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import Http404
from .forms import *
from django.contrib.auth.models import User

# Create your views here.
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
    return render(request, 'a_users/profile.html', {'profile': profile})
@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'a_users/profile_edit.html', {'form': form})

@login_required
def profile_delete_view(request):
    
    if request.method == 'POST':
        user  = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted successfully...!')
        return redirect('/')
    
    return render(request, 'a_users/profile_delete.html')