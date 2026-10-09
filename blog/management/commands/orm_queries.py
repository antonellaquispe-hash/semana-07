"""Run the session queries and report how many SQL queries each one fires.

Steps 4 to 7 of the guide, plus the query counting of steps 9 and 11.
"""
from datetime import date

from django.core.management.base import BaseCommand
from django.db import connection
from django.test.utils import CaptureQueriesContext

from blog import session_queries as q


class Command(BaseCommand):
    help = (
        "Ejecuta las consultas de la sesión (pasos 4 a 7), muestra el "
        "resultado y cuenta las consultas SQL de cada una (pasos 9 y 11)."
    )

    def handle(self, *args, **options):
        cases = [
            ("Paso 4 · todos los artículos", lambda: q.all_posts()),
            ("Paso 4 · un artículo por identificador (pk=1)", lambda: q.post_by_id(1)),
            ("Paso 4 · los publicados", lambda: q.published_posts()),
            ("Paso 4 · los no publicados", lambda: q.draft_posts()),
            ("Paso 5 · título contiene «ORM»", lambda: q.posts_with_title("ORM")),
            (
                "Paso 5 · publicados del 2026-03-01 al 2026-05-31",
                lambda: q.posts_between(date(2026, 3, 1), date(2026, 5, 31)),
            ),
            ("Paso 5 · sin categoría", lambda: q.posts_without_category()),
            ("Paso 5 · con más de 2 comentarios", lambda: q.posts_with_more_than(2)),
            ("Paso 6 · artículos de autores de Perú", lambda: q.posts_by_author_country("Perú")),
            ("Paso 6 · comentarios de «Tecnología»", lambda: q.comments_of_category("Tecnología")),
            ("Paso 7 · los 10 más recientes", lambda: q.latest_posts(10)),
            ("Paso 7 · los 5 más comentados", lambda: q.most_commented_posts(5)),
        ]

        for label, func in cases:
            with CaptureQueriesContext(connection) as captured:
                # The QuerySet is lazy: build it and render it inside the
                # capture block so every SQL query is counted.
                text = self._render(func())
            self.stdout.write(self.style.HTTP_INFO(f"\n{label}"))
            self.stdout.write(text)
            self.stdout.write(
                self.style.SUCCESS(
                    f"  -> {len(captured.captured_queries)} consulta(s) SQL"
                )
            )

    def _render(self, result):
        """Turn a QuerySet, a list or a single object into printable lines."""
        if isinstance(result, (list, tuple)):
            items = list(result)
        elif hasattr(result, "__iter__") and not isinstance(result, str):
            items = list(result)
        else:
            items = [result]

        lines = []
        for obj in items:
            extra = f" ({obj.n_comments} comentarios)" if hasattr(obj, "n_comments") else ""
            lines.append(f"  - {obj}{extra}")
        return "\n".join(lines) if lines else "  (sin resultados)"
