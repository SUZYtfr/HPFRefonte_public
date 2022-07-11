from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin


urlpatterns = [
    path(r"api/", include([
        path(r"users/", include("users.urls", namespace="users")),
        path(r"fictions/", include("fictions.urls", namespace="fictions")),
        path(r"collections/", include("colls.urls", namespace="collections")),
        path(r"features/", include("features.urls", namespace="features")),
        path(r"reviews/", include("reviews.urls", namespace="reviews")),
        path(r"polls/", include("polls.polls_urls", namespace="polls")),
        path(r"selections/", include("selections.urls", namespace="selections")),
        path(r"news/", include("news.urls", namespace="news")),
        path(r"reports/", include("reports.urls", namespace="reports")),
        path(r"images/", include("images.urls", namespace="images")),
        path(r"account/", include("accounts.urls", namespace="accounts")),
    ])),
    path(r"admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
