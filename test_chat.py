from fastapi.testclient import TestClient

from backend.main import app
from backend.security import create_access_token


token = create_access_token(3)

client = TestClient(app)

with client.websocket_connect(
    f"/chat/ws/2?token={token}"
) as websocket:

    message = websocket.receive_json()

    print(message)