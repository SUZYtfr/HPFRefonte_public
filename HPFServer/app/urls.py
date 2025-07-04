from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from app.graphql_api.schema import schema
from strawberry.django.views import GraphQLView

from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path(r"graphql/", csrf_exempt(GraphQLView.as_view(schema=schema)), name="graphql-api"),
    path(r"api/", include([
        path(r"users/", include("users.public_urls", namespace="users")),
        path(r"fictions/", include("fictions.public_urls", namespace="fictions")),
        path(r"characteristics/", include("characteristics.public_urls", namespace="characteristics")),
        path(r"reviews/", include("reviews.urls", namespace="reviews")),
        path(r"news/", include("news.public_urls", namespace="news")),
        # path(r"reports/", include("reports.urls", namespace="reports")),
        path(r"images/", include("images.public_urls", namespace="images")),
        path(r"account/", include("account.urls", namespace="account")),
        path(r"private/", include([
            path(r"users/", include("users.private_urls", namespace="private-users")),
            path(r"fictions/", include("fictions.private_urls", namespace="private-fictions")),
            path(r"news/", include("news.private_urls", namespace="private-news")),
            path(r"characteristics/", include("characteristics.private_urls", namespace="private-characteristics")),
            path(r"images/", include("images.private_urls", namespace="private-images")),
        ])),
    ])),
    path(r"admin/", admin.site.urls),
    path(r'schema/download/', SpectacularAPIView.as_view(), name='schema'),
    path(r"schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-schema'),
    path(r'schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
