import requests

EXTERNAL_API_URL = "https://your-external-api.com/api/matches/"

def get_active_matches():
    response = requests.get(EXTERNAL_API_URL)
    response.raise_for_status()
    return response.json()["matches"]

def post_match_result(match_id, result):
    url = f"{EXTERNAL_API_URL}{match_id}/result/"
    data = {"result": result}
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()