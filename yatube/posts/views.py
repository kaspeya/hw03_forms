from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group, Post, User
from .forms import PostForm


# Главная страница
def index(request):
    template = 'posts/index.html'
    # Сортировка постов по полю pub_date по убыванию.
    posts = Post.objects.all()
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGE_LIMIT)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


# Страница с постами сообщества.
def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    # Сортировка постов по полю pub_date по убыванию.
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:settings.PAGE_LIMIT]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGE_LIMIT)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context, slug)


def paginator(request, post_list):
    paginator = Paginator(post_list, settings.PAGE_LIMIT)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.filter(author__exact=author)
    paginator = Paginator(post_list, settings.PAGE_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'author': author,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post, pk=post_id)
    page_number = request.GET.get('page' or None)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            Post.objects.create(
                text=text,
                group=group,
                author=request.user,
            )
            return redirect('posts:profile', request.user.username)
        return render(request, 'posts/post_create.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})

@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    if request.method == 'POST':
        if form.is_valid():
            post.text = form.cleaned_data['text']
            post.group = form.cleaned_data['group']
            post.save()
            return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'is_edit': is_edit,
    }
    return render(request, 'posts/post_create.html', context)
    form = PostForm()
    return redirect('posts:post_detail', post_id)
