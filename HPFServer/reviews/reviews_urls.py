from django.urls import path, re_path

from .views import ReviewsListCreateView


app_name = "reviews"

urlpatterns = [
    path(r"fictions/<pk>/", ReviewsListCreateView.as_view(), kwargs={"contenttype": "fiction"}, name="fiction-reviews"),
    path(r"chapitres/<pk>/", ReviewsListCreateView.as_view(), kwargs={"contenttype": "chapter"}, name="chapter-reviews"),
    path(r"collections/<pk>/", ReviewsListCreateView.as_view(), kwargs={"contenttype": "collection"}, name="collection-reviews"),
    re_path(r"membres/(?P<pk>\d+)(-.+)?/", ReviewsListCreateView.as_view(), kwargs={"contenttype": "user"}, name="user-reviews"),
]
