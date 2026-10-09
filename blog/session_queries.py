"""The queries of the session procedure (steps 4 to 7 of the guide).

One function per step, each returning a QuerySet (or a model instance). The
management command ``orm_queries`` runs them all, prints the result and counts
how many SQL queries each one fires.
"""
from django.db.models import Count

from blog.models import Comment, Post


def all_posts():
    """Step 4: every article."""
    return Post.objects.all()


def post_by_id(post_id):
    """Step 4: one article by its identifier."""
    return Post.objects.get(pk=post_id)


def published_posts():
    """Step 4: the published articles, through the custom manager."""
    return Post.published_posts.all()


def draft_posts():
    """Step 4: the articles that are not published yet."""
    return Post.objects.filter(published=False)


def posts_with_title(text):
    """Step 5: articles whose title contains a text."""
    return Post.objects.filter(title__icontains=text)


def posts_between(start, end):
    """Step 5: articles published in a range of dates."""
    return Post.objects.filter(published_at__range=(start, end))


def posts_without_category():
    """Step 5: articles with no category assigned."""
    return Post.objects.filter(category__isnull=True)


def posts_with_more_than(n_comments):
    """Step 5: articles with more than a given number of comments."""
    return (
        Post.objects.annotate(n_comments=Count("comments"))
        .filter(n_comments__gt=n_comments)
        .order_by("title")
    )


def posts_by_author_country(country):
    """Step 6: articles written by authors from a country (double underscore)."""
    return Post.objects.filter(author__profile__country=country)


def comments_of_category(name):
    """Step 6: comments of the articles of a category (double underscore)."""
    return Comment.objects.filter(post__category__name=name)


def latest_posts(n=10):
    """Step 7: the n most recent articles."""
    return Post.objects.filter(published_at__isnull=False).order_by("-published_at")[:n]


def most_commented_posts(n=5):
    """Step 7: the n most commented articles, annotated with a count."""
    return Post.objects.annotate(n_comments=Count("comments")).order_by("-n_comments")[:n]
