from decouple import config
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Author, Content
from .utils import get_author_details, get_content_list


@api_view(["GET"])
def content_list(request):
    api_key = config("API_KEY")
    page = request.GET.get("page", 1)

    # Fetch content data from the third-party API
    content_data = get_content_list(api_key, page)

    # Iterate over each content item in the response
    for item in content_data:
        # Extract author data
        author_id = item["author"]["id"]
        author_data = get_author_details(api_key, author_id)

        # Create or update author
        author, _ = Author.objects.get_or_create(
            unique_id=author_id,
            defaults={
                "unique_uuid": author_data.get("unique_uuid", ""),
                "origin_unique_id": author_data.get("origin_unique_id", ""),
                "name": author_data.get("info", {}).get("name", ""),
                "platform": author_data.get("info", {}).get("platform", ""),
                "username": author_data.get("username", ""),
                "followers_count": author_data.get("stats", {})
                .get("digg_count", {})
                .get("followers", {})
                .get("count", 0),
                "avatar_url": author_data.get("avatar", {}).get("urls", [""])[0],
                "profile_text": author_data.get("texts", {}).get("profile_text", ""),
            },
        )

        # Create or update content
        content, _ = Content.objects.update_or_create(
            unique_id=item["unique_id"],
            defaults={
                "unique_uuid": item.get("unique_uuid", ""),
                "origin_unique_id": item.get("origin_unique_id", ""),
                "created_at": item["creation_info"].get("created_at", ""),
                "author": author,
                "main_text": item["context"].get("main_text", ""),
                "token_count": item["context"].get("token_count", 0),
                "char_count": item["context"].get("char_count", 0),
                "tag_count": item["context"].get("tag_count", 0),
                "origin_platform": item["origin_details"].get("origin_platform", ""),
                "origin_url": item["origin_details"].get("origin_url", ""),
                "media_url": item["media"].get("urls", [""])[0],
                "media_type": item["media"].get("media_type", ""),
                "likes_count": item["stats"]["digg_counts"]["likes"].get("count", 0),
                "views_count": item["stats"]["digg_counts"]["views"].get("count", 0),
                "comments_count": item["stats"]["digg_counts"]["comments"].get(
                    "count", 0
                ),
            },
        )

    return JsonResponse({"message": "Content list fetched and updated successfully."})
