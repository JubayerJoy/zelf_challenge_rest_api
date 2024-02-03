from rest_framework.decorators import api_view
from rest_framework.response import Response
from decouple import config
from .utils import get_content_list, get_author_details
from .models import Content, Author

@api_view(['GET'])
def content_list(request):
    api_key =  config('API_KEY');
    page = request.GET.get('page', 1)
    content_data = get_content_list(api_key, page)
    for item in content_data:
        author_data = item['author']
        author_id = author_data['id']
        author_details = get_author_details(api_key, author_id)
        author, _ = Author.objects.get_or_create(
            unique_id=author_details['unique_id'],
            defaults={
                'unique_uuid': author_details['unique_uuid'],
                'origin_unique_id': author_details['origin_unique_id'],
                'name': author_details['info']['name'],
                'platform': author_details['info']['platform'],
                'username': author_details['username'],
                'followers_count': author_details['stats']['digg_count']['followers']['count'],
                'avatar_url': author_details['avatar']['urls'][0],
                'profile_text': author_details['texts']['profile_text']
            }
        )
        Content.objects.get_or_create(
            unique_id=item['unique_id'],
            defaults={
                'unique_uuid': item['unique_uuid'],
                'origin_unique_id': item['origin_unique_id'],
                'created_at': item['creation_info']['created_at'],
                'author': author,
                'main_text': item['context']['main_text'],
                'token_count': item['context']['token_count'],
                'char_count': item['context']['char_count'],
                'tag_count': item['context']['tag_count'],
                'origin_platform': item['origin_details']['origin_platform'],
                'origin_url': item['origin_details']['origin_url'],
                'media_url': item['media']['urls'][0] if item['media']['urls'] else None,
                'media_type': item['media']['media_type'],
                'likes_count': item['stats']['digg_counts']['likes']['count'],
                'views_count': item['stats']['digg_counts']['views']['count'],
                'comments_count': item['stats']['digg_counts']['comments']['count']
            }
        )
    return Response({"message": "Content list fetched successfully."})
