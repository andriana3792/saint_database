from django.urls import path
from . import views
from .views import (
    SaintListView,
    SaintDetailView,
    SaintCreateView,
    SaintUpdateView,
    SaintDeleteView,
)

urlpatterns = [
    path(
        "", SaintListView.as_view(), name="saint-list"
    ),  # root path shows list of saints
    path(
        "saints/", SaintListView.as_view(), name="saint-list-alt"
    ),  # optional alternative URL
    path("saints/<int:pk>/", SaintDetailView.as_view(), name="saint-detail"),
    path("saints/create/", SaintCreateView.as_view(), name="saint-create"),
    path("saints/<int:pk>/update/", SaintUpdateView.as_view(), name="saint-update"),
    path("saints/<int:pk>/delete/", SaintDeleteView.as_view(), name="saint-delete"),
]
