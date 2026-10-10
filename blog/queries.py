"""Queries behind the views. Part 2 of the lab happens in this file."""
from blog.models import Post


def posts_for_front_page():
    # The custom `published` manager replaces the repeated published filter,
    # `select_related` fetches every author and category in the same query, and
    # `prefetch_related` loads all the tags in one extra query: two queries
    # total instead of one per post (N+1).
    return (
        Post.published_posts.select_related("author", "category")
        .prefetch_related("tags")
        .order_by("-published_at")
    )
