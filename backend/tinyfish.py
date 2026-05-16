import json
import os
import time
import requests
from backend.model_utils import get_tinyfish_client

def get_tinyfish_news(): 
    """
    note: using requests instead of tinyfish library because the SDK is still minimal.
    also using single agent (instead of 2) because they don't share context, need articles to not overlap.
    """
    cache_file = "tinyfish_cache.json"
    cache_ttl = 24 * 60 * 60 # 24 hours
    
    if os.path.exists(cache_file):
        file_age = time.time() - os.path.getmtime(cache_file)
        if file_age < cache_ttl:
            try:
                with open(cache_file, "r") as f:
                    print("Loading articles from TinyFish cache...")
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load cache: {e}")

    try: 
        tinyfish_api_key = get_tinyfish_client()
        url = 'https://agent.tinyfish.ai/v1/automation/run-async'

        headers = {
            'X-API-Key': tinyfish_api_key,
            'Content-Type': 'application/json'}

        payload = {
            'url': "https://example.com/task", 
            'goal': "Scrape the most pressing 3 articles and 2 opinion pieces from the last week from CNA, Al Jazeera, CNN and AP. I should only have 7 articles in total. Make sure that the topics do not overlap. Do not summarise the articles, but return the full article text."
        }

        response = requests.post(url, json=payload, headers=headers) #should get run_id and error
        response_json = response.json()
        run_id, error = response_json.get("run_id"), response_json.get("error")
        
        if error != None:
            print(f"There was an error in getting a response: {error}")
            return None
        else: 
            print("Waiting for results...")
            status_url = f"https://agent.tinyfish.ai/v1/runs/{run_id}"
            while True: 
                status_check = requests.get(status_url, headers = headers).json()
                status = status_check.get('status')
                if status == "COMPLETED": 
                    print("Successfully retrieved articles.")
                    result = status_check.get('result')
                    # Save to cache
                    try:
                        with open(cache_file, "w") as f:
                            json.dump(result, f)
                    except Exception as e:
                        print(f"Failed to save cache: {e}")
                    return result
                elif status == "FAILED": 
                    print(f"TinyFish failed to obtain news articles: {status_check.get('error').get('message')}")
                    return None 
                else: 
                    print(f"Task not finished.")
                    time.sleep(40)
    except Exception as e:
        print(f"TinyFish request failed: {e}")
        return None

def load_fixture_articles(path=None):
    path = path or os.getenv("FIXTURE_PATH", "stuff.json")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Unable to load fixture articles from {path}: {e}")
        return None

if __name__ == "__main__": 
    get_tinyfish_news()