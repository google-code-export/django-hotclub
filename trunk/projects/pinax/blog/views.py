from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import date_based
from django.conf import settings

from blog.models import Post
from blog.forms import *
import datetime

try:
    from notification import models as notification
except ImportError:
    notification = None

try:
    from friends.models import Friendship
    friends = True
except ImportError:
    friends = False

def blogs(request):
    blogs = Post.objects.filter(status=2).order_by("-publish")
    return render_to_response("blog/blogs.html", {"blogs": blogs}, context_instance=RequestContext(request))
    
def post(request, username, year, month, slug):
    post = Post.objects.filter(slug=slug, publish__year=int(year), publish__month=int(month)).filter(author__username=username)
    if not post:
        raise Http404
    
    return render_to_response("blog/post.html", {
        "post": post[0],
    }, context_instance=RequestContext(request))

def your_posts(request):
    user = request.user
    blogs = Post.objects.filter(author=user)
    
    return render_to_response("blog/your_posts.html", {"blogs": blogs}, context_instance=RequestContext(request))

@login_required
def new(request):
    if request.method == "POST":
        if request.POST["action"] == "create":
            blog_form = BlogForm(request.user, request.POST)
            if blog_form.is_valid():
                blog = blog_form.save(commit=False)
                blog.author = request.user
                if settings.BEHIND_PROXY:
                    blog.creator_ip = request.META["HTTP_X_FORWARDED_FOR"]
                else:
                    blog.creator_ip = request.META['REMOTE_ADDR']
                blog.save()
                request.user.message_set.create(message="Successfully saved post '%s'" % blog.title)
                if notification:
                    if friends: # @@@ might be worth having a shortcut for sending to all friends
                        notification.send((x['friend'] for x in Friendship.objects.friends_for_user(blog.author)), "blog_friend_post", "%s has posted to their blog.", [blog.author])
                
                return HttpResponseRedirect(reverse("your_posts"))
        else:
            blog_form = BlogForm()
    else:
        blog_form = BlogForm()
    
    return render_to_response("blog/new.html", {
        "blog_form": blog_form
    }, context_instance=RequestContext(request))

@login_required
def edit(request, id):
    post = get_object_or_404(Post, id=id)
    
    if request.method == "POST":
        if post.author != request.user:
            request.user.message_set.create(message="You can't edit posts that aren't yours")
            return HttpResponseRedirect(reverse("your_posts"))
        if request.POST["action"] == "update":
            blog_form = BlogForm(request.user, request.POST, instance=post)
            if blog_form.is_valid():
                blog = blog_form.save(commit=False)
                blog.save()
                request.user.message_set.create(message="Successfully updated post '%s'" % blog.title)
                
                return HttpResponseRedirect(reverse("your_posts"))
        else:
            blog_form = BlogForm(instance=post)
    else:
        blog_form = BlogForm(instance=post)
    
    return render_to_response("blog/edit.html", {
        "blog_form": blog_form,
        "post": post,
    }, context_instance=RequestContext(request))