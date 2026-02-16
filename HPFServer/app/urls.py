from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from app.graphql_api.schema import schema
from strawberry.django.views import GraphQLView

from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path(r"graphql/", csrf_exempt(GraphQLView.as_view(schema=schema)), name="graphql-api"),
    path(r"admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
