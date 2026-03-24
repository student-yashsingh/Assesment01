from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth.models import User
from .models import Post, Comment, Tag, UserProfile
from .forms import RegisterForm, PostForm, CommentForm, UserProfileForm


def home(request):
    posts = Post.objects.filter(status='published').select_related('author').prefetch_related('tags', 'comments', 'author__profile')
    active_tag = None
    tag_slug = request.GET.get('tag')
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    tags = Tag.objects.all()
    return render(request, 'home.html', {
        'page_obj': page_obj,
        'tags': tags,
        'active_tag': active_tag,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.status == 'draft' and post.author != request.user:
        raise Http404

    comments = post.comments.select_related('author', 'author__profile')
    comment_form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment posted!')
            return redirect('post_detail', slug=slug)

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # Save M2M (tags) after the post has a PK
            form.instance = post
            form.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form, 'action': 'Create'})


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form, 'action': 'Edit', 'post': post})


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('my_posts')
    return render(request, 'delete_post.html', {'post': post})


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).prefetch_related('tags', 'comments')
    return render(request, 'my_posts.html', {'posts': posts})


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=profile_user)
    posts = Post.objects.filter(author=profile_user, status='published').prefetch_related('tags', 'comments')

    if request.method == 'POST' and request.user == profile_user:
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=username)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'form': form,
    })


def tag_filter(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(status='published', tags=tag).select_related('author').prefetch_related('tags', 'comments', 'author__profile')
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    tags = Tag.objects.all()
    return render(request, 'home.html', {
        'page_obj': page_obj,
        'tags': tags,
        'active_tag': tag,
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f'Welcome to InkSpace, {user.username}!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
