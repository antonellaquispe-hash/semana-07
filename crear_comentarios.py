import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()

from blog.models import Post, Comment
from datetime import datetime

# Create some sample comments for posts
posts = Post.objects.all()[:3]  # First 3 posts

for post in posts:
    # Create 3 comments per post
    for i in range(1, 4):
        Comment.objects.get_or_create(
            post=post,
            author_name=f'Lector {i}',
            defaults={
                'text': f'Comentario {i} sobre "{post.title}"',
                'created_at': datetime.now()
            }
        )
    print(f'Post: {post.title} - Comments created: 3')

print()
print('Total comentarios en BD:', Comment.objects.count())