from django.urls import include, path
from .views import get_item_by_id

urlpatterns = [
    path("/<int:id>/", get_item_by_id),
]
