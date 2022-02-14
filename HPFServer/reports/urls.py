from rest_framework.urls import path

from .views import ReportCreateView

app_name = "reports"

urlpatterns = [
    path(r"fictions/<pk>/", ReportCreateView.as_view(), kwargs={"contenttype": "fiction"}, name="fiction-report"),
    path(r"chapitres/<pk>/", ReportCreateView.as_view(), kwargs={"contenttype": "chapter"}, name="chapter-report"),
    path(r"membres/<pk>/", ReportCreateView.as_view(), kwargs={"contenttype": "user"}, name="user-report"),
]
