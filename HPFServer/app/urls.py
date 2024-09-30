from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path(r"api/", include([
        path(r"users/", include("users.public_urls", namespace="users")),
        path(r"fictions/", include("fictions.urls", namespace="fictions")),
        path(r"characteristics/", include("characteristics.public_urls", namespace="characteristics")),
        path(r"reviews/", include("reviews.urls", namespace="reviews")),
        path(r"news/", include("news.public_urls", namespace="news")),
        # path(r"reports/", include("reports.urls", namespace="reports")),
        path(r"images/", include("images.urls", namespace="images")),
        path(r"account/", include("account.urls", namespace="account")),
        path(r"private/", include([
            path(r"users/", include("users.private_urls", namespace="private-users")),
            path(r"news/", include("news.private_urls", namespace="private-news")),
            path(r"characteristics/", include("characteristics.private_urls", namespace="private-characteristics")),
        ])),
    ])),
    path(r"admin/", admin.site.urls),
    path(r'schema/download/', SpectacularAPIView.as_view(), name='schema'),
    path(r"schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-schema'),
    path(r'schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
