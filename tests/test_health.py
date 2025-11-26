import os
import requests

def test_health_endpoint():
    base = os.getenv("BASE_URL", "http://localhost:8000")
    r = requests.get(f"{base}/api/health", timeout=5)
    assert r.status_code == 200
    j = r.json()
    assert j.get("ok") is True
