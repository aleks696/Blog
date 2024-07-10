from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Likes, Comments
from .forms import CommentsForm, PostForm
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied

@login_required
def post_view(request):
    """ Posts Page """
    posts = Post.objects.all()
    return render(request, 'blog.html', {'post_list': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog_detail.html', {'post': post})

@login_required
@require_http_methods(["GET", "POST"])
def create_post_view(request):
    """ Create post """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.username
            post.save()
            return redirect('posts')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})

@login_required
@require_http_methods(["GET", "POST"])
def edit_post_view(request, pk):
    """ Edit post """
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user.username:
        raise PermissionDenied("You don't have rights to edit this post!")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
@require_http_methods(["GET"])
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_superuser or post.author == request.user.username:
        post.delete()
        return redirect('posts')
    else:
        raise PermissionDenied("You are not allowed to delete this post.")

def search_posts(request):
    """ Search posts by title """
    query = request.GET.get('q')
    if query:
        post_list = Post.objects.filter(title__icontains=query)
    else:
        post_list = Post.objects.all()

    return render(request, 'blog.html', {'post_list': post_list})

@login_required
@require_http_methods(["POST"])
def add_comments(request, pk):
    form = CommentsForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = get_object_or_404(Post, pk=pk)
        parent_id = request.POST.get('parent_id')
        if parent_id:
            comment.parent = Comments.objects.get(id=parent_id)
        if request.user.is_authenticated:
            comment.name = request.user.username
            comment.email = request.user.email
        comment.save()
    return redirect('post_detail', pk=pk)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
@require_http_methods(["GET"])
def add_like(request, pk):
    ip_client = get_client_ip(request)
    try:
        Likes.objects.get(ip=ip_client, pos_id=pk)
    except Likes.DoesNotExist:
        new_like = Likes(ip=ip_client, pos_id=pk)
        new_like.save()
    return redirect('post_detail', pk=pk)

@login_required
@require_http_methods(["GET"])
def dislike(request, pk):
    ip_client = get_client_ip(request)
    try:
        lik = Likes.objects.get(ip=ip_client, pos_id=pk)
        lik.delete()
    except Likes.DoesNotExist:
        pass
    return redirect('post_detail', pk=pk)
