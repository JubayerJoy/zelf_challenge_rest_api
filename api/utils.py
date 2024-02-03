import time

import requests
from decouple import config

from api.rate_limiter import RateLimiter, RateLimitExceededException

CAPACITY = int(config("CAPACITY"))
REFILL_RATE = CAPACITY / int(config("REFILL_TIME"))
MAX_RETRIES = 5
RETRY_DELAY = 1  # in seconds

limiter = RateLimiter(capacity=CAPACITY, refill_rate=REFILL_RATE)


"""
This function makes an API call to the given URL with the given headers and API key.
If the request fails with an HTTP error or due to rate limit, it waits for RETRY_DELAY seconds and tries again.
This is useful for handling rate limits and other temporary issues with the API.
"""


def api_call(invoker_name, url, headers):
    retry_count = 0
    while retry_count <= MAX_RETRIES:
        try:
            if limiter.make_request():
                print(f"Making request from {invoker_name} to {url}...")
                response = requests.get(url, headers=headers)

                if (
                    response.raise_for_status()
                    or type(response) is type(None)
                    or response.status_code != 200
                ):
                    raise Exception(
                        f"Failed to get response from {url}, retrying in {RETRY_DELAY} second(s)..."
                    )

                return response
            else:
                raise RateLimitExceededException(
                    f"Rate limit reached. Waiting for {RETRY_DELAY} second(s) before making another request from {invoker_name} to {url}"
                )
        except Exception as e:
            print(f"Error: {e} {response}")
            retry_count += 1
            if retry_count <= MAX_RETRIES:
                print(
                    f"Retry {retry_count} failed for {url}, retrying in {RETRY_DELAY} second(s)..."
                )
                time.sleep(RETRY_DELAY)
            else:
                # TODO: Maximum retries reached, throw a big alert
                print(
                    f"{url} has reached maximum retry limit, skipping and throwing a big alert..."
                )
                raise  # Rethrow the exception to stop further execution


def get_author_details(api_key, author_id):
    url = f"https://hackapi.hellozelf.com/backend/api/v1/authors/{author_id}"
    headers = {"x-api-key": api_key}

    response = api_call("get_author_details", url, headers=headers)

    author_data = response.json().get("data", {})
    return author_data


def get_content_list(api_key, page=1):
    url = f"https://hackapi.hellozelf.com/backend/api/v1/contents?page={page}"
    headers = {"x-api-key": api_key}

    response = api_call("get_content_list", url, headers=headers)

    data = response.json()
    content_list = data.get("data", [])

    next_page_number = data.get("next")
    if next_page_number:
        content_list += get_content_list(api_key, next_page_number)

    return content_list
