from urllib import response
from base64 import b64encode
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash
from unittest.mock import patch


def test_register(client):
     data = {
          "email":"danielleyurit.santos@gmail.com",
          "password":"123",
     }

     response = client.post("/api/auth/register", data=data)
     result = response.get_json()
     assert result["message"] == "Usuario registrado com sucesso!"

@patch("app.resources.auth.create_access_token")
def test_login(create_access_token_mock, client):
     create_access_token_mock.return_value = "oi123"
     #add user to database
     user = User(email="danielleyurit.santos@gmail.com", password=generate_password_hash("123"))
     db.session.add(user)
     db.session.commit()
     headers = {
          "Authorization":"Basic" + b64encode(b"danielleyurit.santos@gmail.com:123").decode()
     }
     response = client.get("/api/auth/login", headers=headers)
     result = response.get_json()
     token = result["access_token"]
     assert token =="oi123"