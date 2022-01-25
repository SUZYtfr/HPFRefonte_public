from rest_framework.routers import SimpleRouter
from .views import MyPollViewSet, MyPollAnswerViewSet

app_name = "mypolls"

mypolls_router = SimpleRouter()
mypolls_router.register(r"pollquestions", MyPollViewSet, basename="mypoll")

mypollanswers_router = SimpleRouter()
mypollanswers_router.register(r"pollanswers", MyPollAnswerViewSet, basename="mypollanswer")

urlpatterns = mypolls_router.urls + mypollanswers_router.urls
