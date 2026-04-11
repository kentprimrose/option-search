from django.urls import include, path

urlpatterns = [
    path("", include("screener.urls")),
]
