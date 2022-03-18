from django.urls import path, include
from rest_framework.routers import SimpleRouter

from features.views import BookshelfViewSet, ShelvedElementListRetrieveDestroyViewSet
from .views import UserViewSet


app_name = "users"

users_router = SimpleRouter()
users_router.register(r"", viewset=UserViewSet, basename=r"user")
bookshelf_router = SimpleRouter()
bookshelf_router.register(r"", viewset=BookshelfViewSet)
shelvedelement_router = SimpleRouter()
shelvedelement_router.register(r"", viewset=ShelvedElementListRetrieveDestroyViewSet)

urlpatterns = [
    path(r"<user_pk>/bookshelves/<bookshelf_pk>/elements/", include(shelvedelement_router.urls)),
    path(r"<user_pk>/bookshelves/", include(bookshelf_router.urls)),
] + users_router.urls
