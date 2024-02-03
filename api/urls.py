from django.urls import path

from . import views

urlpatterns = [
    path(
        "content-with-author/",
        views.get_content_with_author,
        name="get_content_with_author",
    ),
    # Other URL patterns
]
