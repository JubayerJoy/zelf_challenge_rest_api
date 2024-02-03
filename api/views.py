import json

import redis
from decouple import config
from django.http import JsonResponse

REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")


def get_content_with_author(request):
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    # Retrieve content data from Redis
    content_data = redis_client.hget("api_data", "content_data")
    if content_data:
        contents = json.loads(content_data)
    else:
        return JsonResponse({"error": "No content data found in Redis"})

    # Retrieve author data from Redis
    author_data = redis_client.hget("api_data", "author_data")
    if author_data:
        authors = json.loads(author_data)
    else:
        return JsonResponse({"error": "No author data found in Redis"})

    # Combine content and author data
    contents_with_author = []
    for content in contents:
        if isinstance(content, dict):
            author_id = content.get("author_id")
            # Iterate over the nested lists of authors
            for author_list in authors:
                for author_dict in author_list:
                    if author_dict.get("unique_id") == author_id:
                        content["author"] = author_dict
                        contents_with_author.append(content)
                        break
                else:
                    continue
                break
        else:
            return JsonResponse({"error": "Invalid content data format in Redis"})

    return JsonResponse(contents_with_author, safe=False)
