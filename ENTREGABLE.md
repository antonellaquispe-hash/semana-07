# Entregable — ORM de Django (semana 07)

Registro de las consultas del procedimiento de la sesión, sus resultados y el
número de consultas SQL que dispara cada una. Código, nombres y comentarios en
inglés; explicaciones en español.

Cómo reproducirlo:

```bash
python manage.py migrate
python manage.py seed_blog        # datos fijos: 4 autores, 15 artículos, 23 comentarios
python manage.py orm_queries      # corre las consultas y cuenta las consultas SQL
python manage.py test
```

## Datos de partida (paso 3)

| Dato | Cantidad |
|---|---|
| Autores | 4 (2 de Perú, 2 de Chile) |
| Artículos | 15 (11 publicados, 4 borradores) |
| Artículos con comentarios | 11 de 15 |
| Comentarios | 23 |
| Categorías | 4 (Tecnología, Cultura, Deportes, Opinión) |
| Etiquetas | 5 (django, python, orm, noticias, tutorial) |

## Cumplimiento del procedimiento

| Paso | Qué pide | Dónde está | Estado |
|---|---|---|---|
| 1 | Proyecto con la estructura del curso, `blog` en `INSTALLED_APPS`, plantillas y estáticos, Pillow | `config/settings.py`, `blog/templates/`, `static/`, `requirements.txt` | ✅ |
| 2 | Modelos `Author`, `Post`, `Category`, `Tag`, `Comment` + antero/`Profile` y migración | `blog/models.py`, `blog/migrations/0001_initial.py` | ✅ |
| 3 | Datos: ≥3 autores, 15 artículos, categorías, etiquetas y comentarios en la mitad | `blog/seed_data.py`, `manage.py seed_blog` | ✅ |
| 4 | Consola: todos, uno por id, publicados y no publicados | `blog/session_queries.py` (`all_posts`, `post_by_id`, `published_posts`, `draft_posts`) | ✅ |
| 5 | Búsquedas por campo: `icontains`, `range`, `isnull`, `annotate`+`Count` | `posts_with_title`, `posts_between`, `posts_without_category`, `posts_with_more_than` | ✅ |
| 6 | Relaciones con doble guion bajo: país del autor y categoría de los comentarios | `posts_by_author_country`, `comments_of_category` | ✅ |
| 7 | Ordenar y limitar: 10 más recientes y 5 más comentados | `latest_posts`, `most_commented_posts` | ✅ |
| 8 | Manager propio de `Post` para los publicados y usarlo en las vistas | `blog/models.py` (`PublishedManager` → `Post.published_posts`), `blog/queries.py` | ✅ |
| 9 | Registro de consultas SQL y recorrer los artículos mostrando el autor | `config/settings.py` (`LOGGING`), `blog/templates/blog/front_page.html` | ✅ |
| 10 | `select_related` + `prefetch_related` y comparar el número de consultas | `blog/queries.py` (ver tabla siguiente) | ✅ |
| 11 | Registrar cada consulta, su resultado y el número de consultas | este documento | ✅ |

## Registro de consultas (pasos 4 a 7 y 11)

| # | Consulta | Lookup / ORM | Resultado | Filas | Consultas SQL |
|---|---|---|---|---|---|
| 1 | Todos los artículos | `Post.objects.all()` | todos | 15 | 1 |
| 2 | Un artículo por id | `Post.objects.get(pk=1)` | «Introducción al ORM de Django» | 1 | 1 |
| 3 | Publicados | `Post.published_posts.all()` | publicados | 11 | 1 |
| 4 | No publicados | `filter(published=False)` | borradores | 4 | 1 |
| 5 | Título contiene «ORM» | `title__icontains` | «Introducción al ORM de Django» | 1 | 1 |
| 6 | Rango de fechas | `published_at__range` | 2026-03-01 … 2026-05-31 | 9 | 1 |
| 7 | Sin categoría | `category__isnull=True` | 2 artículos | 2 | 1 |
| 8 | Más de 2 comentarios | `annotate(Count("comments"))` | 6, 4 y 3 comentarios | 3 | 1 |
| 9 | Autores de Perú | `author__profile__country` | publicados y borradores | 12 | 1 |
| 10 | Comentarios de «Tecnología» | `post__category__name` | incluye el comentario hostil | 17 | 1 |
| 11 | 10 más recientes | `order_by("-published_at")[:10]` | — | 10 | 1 |
| 12 | 5 más comentados | `annotate(Count("comments")).order_by("-n_comments")[:5]` | — | 5 | 1 |

Cada consulta aislada gasta **1 consulta SQL** (nada se filtra ni se ordena en
Python).

## Pasos 9 y 10 — conteo de consultas en la portada

La portada recorre los artículos publicados y, por cada uno, lee su autor
(`post.author`) y sus etiquetas (`post.tags.all`). Medido con
`CaptureQueriesContext` sobre `GET /`:

| Versión | Consultas | Detalle |
|---|---|---|
| Antes (N+1) | **23** | 1 (artículos) + 11 (autores) + 11 (etiquetas) |
| Después | **2** | `select_related("author")` + `prefetch_related("tags")` |

La prueba `blog/tests/test_front_page.py::test_front_page_runs_two_queries`
verifica que se mantengan en 2.
