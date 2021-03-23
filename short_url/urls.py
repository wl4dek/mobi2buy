from django.urls import path
from .views import UrlList, UrlCreate, UrlRedirect

urlpatterns = [
    path("url/", UrlList.as_view(), name="list"),
    path("url/create/", UrlCreate.as_view(), name="create"),
    path("url/<name>/", UrlRedirect.as_view(), name="retrive"),
]
