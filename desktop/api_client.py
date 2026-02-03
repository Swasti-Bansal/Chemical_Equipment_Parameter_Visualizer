import requests

BASE = "http://127.0.0.1:8000/api"   # ✅ correct base

ACCESS_TOKEN = None
REFRESH_TOKEN = None

def login(username, password):
    global ACCESS_TOKEN, REFRESH_TOKEN

    r = requests.post(
        f"{BASE}/login/",            # ✅ correct endpoint
        json={"username": username, "password": password},
        timeout=10
    )

    if r.status_code != 200:
        raise Exception(r.text)

    data = r.json()
    ACCESS_TOKEN = data["access"]
    REFRESH_TOKEN = data["refresh"]
    return data

def auth_headers():
    if not ACCESS_TOKEN:
        raise Exception("Not logged in")
    return {"Authorization": f"Bearer {ACCESS_TOKEN}"}

def download_report(save_path):
    r = requests.get(f"{BASE}/report/", headers=auth_headers(), stream=True, timeout=30)
    if r.status_code != 200:
        raise Exception(f"Report error: {r.status_code} {r.text}")

    with open(save_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def get_history():
    r = requests.get(f"{BASE}/history/", headers=auth_headers(), timeout=20)
    if r.status_code != 200:
        raise Exception(f"History error: {r.status_code} {r.text}")
    return r.json()

def upload_csv(path):
    with open(path, "rb") as f:
        files = {"file": f}
        r = requests.post(f"{BASE}/upload/", files=files, headers=auth_headers(), timeout=60)

    if r.status_code not in (200, 201):
        raise Exception(f"Upload error: {r.status_code} {r.text}")
    return r.json()
