# api/utils.py
import requests

def get_content_list(api_key, page=1):
    url = f"https://hackapi.hellozelf.com/backend/api/v1/contents?page={page}"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    return response.json()

def get_author_details(api_key, author_id):
    url = f"https://hackapi.hellozelf.com/backend/api/v1/authors/{author_id}"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    return response.json()
