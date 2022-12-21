from django.core.management.base import BaseCommand, CommandError
from tests.samples import (
    sample_user,
    sample_fiction,
    sample_news,
    sample_comment,
    sample_fiction_review,
)


class Command(BaseCommand):
    help = "Crée de fausses données"

    def add_arguments(self, parser):
        parser.add_argument(
            "model",
            choices=["user", "fiction", "news", "comment", "fictionreview"],
        )
        parser.add_argument(
            "-c",
            "--count",
            nargs="?",
            default=1,
            type=int,
            metavar="NOMBRE",
            help="Nombre d'éléments à générer",
        )
        parser.add_argument(
            "-p",
            "--parent",
            nargs="?",
            default=None,
            type=int,
            metavar="ID",
            help="ID de l'élément parent",
        )

    def handle(self, *args, **options):
        corres = {
            "user": (sample_user, None),
            "fiction": (sample_fiction, None),
            "news": (sample_news, None),
            "comment": (sample_comment, "newsarticle_id"),
            "fictionreview": (sample_fiction_review, "fiction_id"),
        }

        model = options["model"]
        count = options["count"]
        parent_id = options["parent"]
        sample_func, parent = corres[model]

        kwargs = {}

        if parent_id:
            if parent:
                kwargs[parent] = parent_id
            else:
                self.stdout.write(self.style.WARNING(f"ID de l'élément parent ignoré pour la création de {model}."))

        else:
            if parent:
                raise CommandError(f"ID de l'élément parent requis pour la création de {model}.")

        for i in range(count):
            try:
                element = sample_func(**kwargs)
                self.stdout.write(self.style.SUCCESS(f"Création de {str(element)}."))
            except Exception as e:
                raise CommandError(f"Échec de la création de fausses données: {e}.")
