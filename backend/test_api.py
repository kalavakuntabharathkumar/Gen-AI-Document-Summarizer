from fastapi.testclient import TestClient
from .main import app
from .security import create_demo_user

client = TestClient(app)

def test_login_and_unauth_upload_blocked():
    r = client.post('/login')
    assert r.status_code == 200
    token = r.json()['token']

    # Without token -> 401
    with open(__file__, 'rb') as f:
        r2 = client.post('/upload', files={'file': ('x.txt', f, 'text/plain')})
    assert r2.status_code == 401

    # With token -> 200 queue
    headers = {'Authorization': f'Bearer {token}'}
    with open(__file__, 'rb') as f:
        r3 = client.post('/upload', files={'file': ('x.txt', f, 'text/plain')}, headers=headers)
    assert r3.status_code == 200
    assert 'document_id' in r3.json()
