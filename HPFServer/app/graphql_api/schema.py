import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from app.graphql_api.queries import Query
from app.graphql_api.mutations import Mutation


""" 
TODO :
- permission IsOwner(target_fields=[creation_user, authors, etc.]) (ex. ChapterVersion)
- exceptions mieux définies ? IllogicalActionError ?
- Session data corrupted??
- choix du meilleur système pour les accès:
    - routes séparées (/graphql/public/, /graphql/private/, /graphql/admin/)
    - racines séparées (published_fictions, private_fictions, admin_fictions) *
    - unique, accès de champs par filtres et permissions
- relié : champs protégés par permissions: erreur globale* ou erreur de champ ?
- schema compilé et servi en live genre comme fait spectacular ?
- filtres, ordonnations sur tous les types ? comment éviter une dép circ entre filters.py et types.py?
- pourquoi ordering ne marche pas avec offset_paginated + resolver, alors que order marche?
- silk ou similaire pour optimiser les requêtes notamment au regard des nombreux getters

* appliqué pour le moment
"""


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
