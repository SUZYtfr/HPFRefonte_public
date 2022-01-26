from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from rest_framework_simplejwt.views import (
   TokenObtainPairView,
   TokenRefreshView,
)

urlpatterns = [
    path(r"api/", include([
        # URLS PUBLIQUES
        path(r"users/", include("users.urls", namespace="users")),
        path(r"fictions/", include("fictions.fictions_urls", namespace="fictions")),
        path(r"chapters/", include("fictions.chapters_urls", namespace="chapters")),
        path(r"collections/", include("colls.collections_urls", namespace="collections")),
        path(r"features/", include("features.urls", namespace="features")),
        path(r"categories/", include("features.categories_urls", namespace="categories")),
        path(r"reviews/", include("reviews.reviews_urls", namespace="reviews")),
        path(r"polls/", include("polls.polls_urls", namespace="polls")),
        path(r"selections/", include("selections.urls", namespace="selections")),
        path(r"news/", include("news.urls", namespace="news")),
        path(r"reports/", include("reports.urls", namespace="reports")),
        path(r"banners/", include("banners.urls", namespace="banners")),

        # URLS PRIVÉES
        path(r"account/", include([
            path(r"", include("accounts.urls", namespace="accounts")),
            path(r"token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
            path(r"token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
            path(r"fictions/", include("fictions.myfictions_urls", namespace="myfictions")),
            path(r"chapters/", include("fictions.mychapters_urls", namespace="mychapters")),
            path(r"collections/", include("colls.mycollections_urls", namespace="mycollections")),
            path(r"my-reviews/", include("reviews.myreviews_urls", namespace="myreviews")),
            path(r"reviews/", include("reviews.reviewsonme_urls", namespace="reviewsonme")),
            path(r"betas/", include("fictions.betas_urls", namespace="betas")),
            path(r"polls/", include("polls.mypolls_urls", namespace="mypolls")),
        ])),
    ])),
    path(r"admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
