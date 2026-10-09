import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()

from blog.models import Post, Author, Category, Tag, Comment
from django.db.models import Count
from datetime import date

print('=== PUNTO 5: Consultas por campo ===')
print()

print('1. Búsqueda por título (__icontains):')
results = Post.objects.filter(title__icontains='Django')
print(f'Títulos con "Django": {results.count()}')
for p in results:
    print(f'  - {p.title}')

print()
print('2. Rango de fechas (__range):')
start = date(2026, 3, 1)
end = date(2026, 5, 31)
results = Post.objects.filter(published_at__range=(start, end))
print(f'Publicaciones entre {start} y {end}: {results.count()}')
for p in results:
    print(f'  - {p.title} (fecha: {p.published_at})')

print()
print('3. Artículos sin categoría (category__isnull=True):')
results = Post.objects.filter(category__isnull=True)
print(f'Total: {results.count()}')
for p in results:
    print(f'  - {p.title}')

print()
print('4. Artículos con más de N comentarios (annotate con Count):')
results = Post.objects.annotate(num_comments=Count('comments')).filter(num_comments__gt=2)
print(f'Posts con más de 2 comentarios: {results.count()}')
for p in results:
    print(f'  - {p.title}: {p.num_comments} comentarios')