import json
import time
import traceback
from datetime import datetime

import redis
from decouple import config

from api.utils import get_author_details, get_content_list

REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")

CRON_JOB_INTERVAL = 10  # in seconds


def fetch_and_store_data():
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    while True:
        try:
            print("Fetching data from API and storing in Redis... 🤖")
            start_time = time.time()
            current_datetime = datetime.fromtimestamp(start_time)
            formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
            print(f"Start time: {formatted_datetime}")

            contents = get_content_list(config("API_KEY"))
            print(f"Fetched {len(contents)} contents from the API")

            # create a set of unique authors
            unique_authors = set()
            for content in contents:
                author_id = content["author"]["id"]
                unique_authors.add(author_id)

            # fetch author details
            authors = []
            for author_id in unique_authors:
                author = get_author_details(config("API_KEY"), author_id)
                authors.append(author)

            print(f"Fetched {len(authors)} authors from the API")

            # Serialize data to JSON
            contents_json = json.dumps(contents)
            authors_json = json.dumps(authors)

            # Store data in Redis
            redis_client.hset("api_data", "content_data", contents_json)
            redis_client.hset("api_data", "author_data", authors_json)
            redis_client.set("last_updated", time.time())

            print("Data fetched and stored in Redis 🎉🎉🎉")
            finish_time = time.time()
            current_datetime = datetime.fromtimestamp(finish_time)
            formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")

            print(
                f"End time: {formatted_datetime}, time taken: {round(finish_time - start_time, 5)} seconds"
            )
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

        print(
            f"Sleeping for {CRON_JOB_INTERVAL} seconds, before fetching data again... 🛌💤"
        )
        time.sleep(CRON_JOB_INTERVAL)


if __name__ == "__main__":
    fetch_and_store_data()
