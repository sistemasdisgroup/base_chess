import requests


def login(base_url: str, user: str, password: str) -> str:
    url = f"{base_url}/auth/login"
    payload = {
        "usuario": user,
        "password": password
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    session_id = response.json()["sessionId"]
    cookie_header = session_id.replace("JSESSIONID-", "JSESSIONID=", 1)
    return cookie_header


def get(base_url: str, endpoint: str, user: str, password: str, params: dict | None = None):
    cookie_header = login(base_url, user, password)

    headers = {
        "Accept": "application/json",
        "Cookie": cookie_header
    }

    url = f"{base_url}/{endpoint}"
    response = requests.get(url, headers=headers, params=params, timeout=60)
    response.raise_for_status()
    return response.json()