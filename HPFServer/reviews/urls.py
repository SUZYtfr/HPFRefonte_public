from rest_framework.routers import SimpleRouter

from .views import ReviewViewset

app_name = "reviews"

review_router = SimpleRouter()
review_router.register(r"reviews", ReviewViewset, basename="review")

urlpatterns = review_router.urls
