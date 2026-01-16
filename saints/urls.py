from django.urls import path
from .views import SaintListView, SaintDetailView

urlpatterns = [
    path("", SaintListView.as_view(), name="saint-list"),
    path("saints/<int:pk>/", SaintDetailView.as_view(), name="saint-detail"),
]
