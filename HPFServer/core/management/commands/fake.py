from django.core.management.base import BaseCommand
from tests.samples import sample_user, sample_fiction, sample_news


class Command(BaseCommand):
    help = "Crée de fausses données"

    def add_arguments(self, parser):
        parser.add_argument(
            "model",
            choices=["user", "fiction", "news"],
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

    def handle(self, *args, **options):
        corres = {
            "user": sample_user,
            "fiction": sample_fiction,
            "news": sample_news,
        }

        for i in range(options["count"] or 1):
            try:
                element = corres[options["model"]]()
                self.stdout.write(self.style.SUCCESS(f"Création de {str(element)}."))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Échec de la création de fausses données: {e}."))
