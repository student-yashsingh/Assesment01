from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from .models import Post, Tag, Comment, UserProfile
from .forms import RegisterForm, PostForm, CommentForm, UserProfileForm
from django.core.paginator import Paginator


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
                return render(request, 'blog/register.html', {'form': form})

            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created! Please sign in.')
            return redirect('login')

    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'blog/login.html')

def home(request):
    tag_slug = request.GET.get('tag')
    posts = Post.objects.filter(status='published')

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=tag)

    featured = posts.first()
    posts = posts.exclude(id=featured.id) if featured else posts

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    tags = Tag.objects.all()

    return render(request, 'blog/home.html', {
        'posts': posts,
        'featured': featured,
        'tags': tags,
        'tag_slug': tag_slug,
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.all()
    form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment posted!')
            return redirect('post_detail', slug=slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

@login_required(login_url='login')
def post_create(request):
    form = PostForm()
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)

            if Post.objects.filter(slug=post.slug).exists():
                messages.error(request, 'A post with this title already exists.')
                return render(request, 'blog/post_form.html', {'form': form, 'tags': tags})

            post.save()
            form.save_m2m()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', slug=post.slug)
        else:
            print(form.errors)

    return render(request, 'blog/post_form.html', {'form': form, 'tags': tags})

@login_required(login_url='login')
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    tags = Tag.objects.all()
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', slug=post.slug)
        else:
            print(form.errors)

    return render(request, 'blog/post_form.html', {
        'form': form,
        'post': post,
        'tags': tags,
    })


@login_required(login_url='login')
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('my_posts')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required(login_url='login')
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    
    total = posts.count()
    published = posts.filter(status='published').count()
    drafts = posts.filter(status='draft').count()

    return render(request, 'blog/my_posts.html', {
        'posts': posts,
        'total': total,
        'published': published,
        'drafts': drafts,
    })


def profile(request, username):
    user = get_object_or_404(User, username=username)
    
    try:
        user_profile = user.profile
    except UserProfile.DoesNotExist:
        user_profile = None

    posts = Post.objects.filter(author=user, status='published')

    return render(request, 'blog/profile.html', {
        'profile_user': user,
        'user_profile': user_profile,
        'posts': posts,
    })

@login_required(login_url='login')
def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(instance=profile)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', username=request.user.username)

    return render(request, 'blog/profile_edit.html', {'form': form})