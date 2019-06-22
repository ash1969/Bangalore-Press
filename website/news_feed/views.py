from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader, RequestContext
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import ContentFile
from PIL import Image
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import *
from django.utils import timezone
from datetime import datetime, timedelta, date
from user_profile.models import *

@login_required
def open_feed(request):
    current_date = timezone.now()
    start_date = current_date + timedelta(days=-2)
    end_date = current_date + timedelta(days=4)  # Using this to display posts
    posts = Post.objects.filter(updated_at__range=[start_date, end_date]).order_by('updated_at')
    upvotes = Upvotes.objects.all()
    profiles = Profile.objects.all()
    args = {'posts': posts, 'upvotes': upvotes, 'profiles': profiles }
    return render(request, 'posts/feed.html', args)


@login_required
def new_post(request):
    form = Postform(request.POST or None, request.FILES or None)

    if request.method=='POST':
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            form.save()
            return redirect('news_feed:open_feed')

    return render(request, 'posts/post-form.html', {'form': form,})

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)
    form = Postform(request.POST or None, request.FILES or None,  instance=post)

    if request.method=='POST':
        if form.is_valid() and post.user==request.user:
            f = form.save(commit=False)
            f.user = request.user
            form.save()
            return redirect('news_feed:open_feed')

    return render(request, 'posts/post-form.html', {'form': form, })

@login_required
def edit_voting(request, id):
    try:
        post = get_object_or_404(Post, pk=id)
    except:
        return HttpResponse("No such post exist!")
    user = request.user
    if Upvotes.objects.filter(post=post, user=user).exists():
            upvote = Upvotes.objects.get(post=post, user=user)
            upvote.delete()
    else:
            upvote = Upvotes.objects.create(post=post, user=user)
            upvote.save()
    return redirect ('news_feed:open_feed')