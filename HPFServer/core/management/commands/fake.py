from django.core.management.base import BaseCommand, CommandError
from core.management.utils.samples import (
    sample_user,
    sample_collection,
    sample_fiction,
    sample_chapter,
    sample_news,
    sample_comment,
    sample_collection_review,
    sample_fiction_review,
    sample_chapter_review,
)


class Command(BaseCommand):
    help = "Crée de fausses données"

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            nargs="?",
            default=1,
            type=int,
            metavar="NOMBRE",
            help="Nombre d'éléments à générer",
        )
        parser.add_argument(
            "model",
            choices=[
                "users",
                "collections",
                "fictions",
                "chapters",
                "news",
                "comments",
                "collection-reviews",
                "fiction-reviews",
                "chapter-reviews",
            ],
            type=str,
            metavar="MODÈLE",
            help="Modèle à générer"
        )
        parser.add_argument(
            "-p",
            "--parent",
            default=None,
            type=int,
            metavar="ID",
            help="ID de l'élément parent",
        )
        parser.add_argument(
            "-u",
            "--user",
            default=None,
            type=int,
            metavar="CRÉATEUR",
            help="ID de l'utilisateur créateur",
        )
        parser.add_argument(
            "-i",
            "--images",
            default=None,
            type=int,
            metavar="IMAGES",
            help="Nombre d'images de contenu à insérer",
        )

    def handle(self, *args, **options):
        corres = {
            "users": (sample_user, None),
            "collections": (sample_collection, None),
            "fictions": (sample_fiction, None),
            "chapters": (sample_chapter, "fiction_id"),
            "news": (sample_news, None),
            "comments": (sample_comment, "newsarticle_id"),
            "collection-reviews": (sample_collection_review, "collection_id"),
            "fiction-reviews": (sample_fiction_review, "fiction_id"),
            "chapter-reviews": (sample_chapter_review, "chapter_id"),
        }

        model = options["model"]
        count = options["count"]
        parent_id = options["parent"]
        creation_user_id = options["user"]
        image_count = options["images"]
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

        if creation_user_id:
            kwargs["creation_user_id"] = creation_user_id

        if image_count:
            kwargs["image_count"] = image_count

        for i in range(count):
            try:
                element = sample_func(**kwargs)
                self.stdout.write(self.style.SUCCESS(f"Création de « {str(element)} »."))
            except Exception as e:
                raise CommandError(f"Échec de la création de fausses données: {e}.")
