from .views import PersonalReviewsListView
from django.urls import path

app_name = "myreviews"

urlpatterns = [
    path(r"", PersonalReviewsListView.as_view()),
]