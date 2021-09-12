from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Count
from django.db.models import Q
from django.views.generic import ListView, DetailView


class PostList(ListView):
    model = Post
    # paginate_by="5"
    queryset = Post.published.all()
    context_object_name = "posts"
    template_name = "blog/post_list.html"


def post_list(request, tag_slug=None):
    posts = Post.published.all()

    # post tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    # search
    query = request.GET.get("q")
    if query:
        posts = Post.published.filter(
            Q(title__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()

    paginator = Paginator(posts, 10)  # 10 posts in each page
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(
        request, "blog/post_list.html", {"posts": posts, page: "pages", "tag": tag}
    )


class PostDetail(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status="published")

    # List of similar posts
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:6]

    return render(
        request, "blog/post_detail.html", {"post": post, "similar_posts": similar_posts}
    )
