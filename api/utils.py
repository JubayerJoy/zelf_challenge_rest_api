# api/utils.py
import requests


def get_author_details(api_key, author_id):
    url = f"https://hackapi.hellozelf.com/backend/api/v1/authors/{author_id}"
    headers = {"x-api-key": api_key}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    author_data = response.json().get("data", {})
    return author_data


def get_content_list(api_key, page=1):
    url = f"https://hackapi.hellozelf.com/backend/api/v1/contents?page={page}"
    headers = {"x-api-key": api_key}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    content_list = data.get("data", [])

    next_page = data.get("next")
    if next_page:
        next_page_number = int(next_page.split("=")[-1])
        content_list += get_content_list(api_key, next_page_number)

    return content_list
