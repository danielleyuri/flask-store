import email
import logging

from app.extensions import db
from app.models import User
from app.services.mail import send_mail

from flask import request
from datetime import timedelta
import secrets

from base64 import b64decode
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import create_access_token


class Login(Resource):

    def get(self):
        if not request.headers.get("Authorization"):
            return {"error": "authorization nao encontrado."}, 400

        basic, code = request.headers["Authorization"].split(" ")
        if not basic.lower() == "basic":
            return {"error": "autorizacao mal formatada."}, 400

        email, password = b64decode(code).decode().split(":")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return {"error": "login e senha invalidos"}, 400

        token = create_access_token(
            {"id": user.id}, expires_delta=timedelta(days=10))

        return {"access_token": token}


class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True,
                            help="o campo e-mail e obrigatorio")
        parser.add_argument("password", required=True,
                            help="o campo password e obrigatorio")
        args = parser.parse_args()

        user = User.query.filter_by(email=args.email).first(
        )  # select id, email, password from users where email =""""
        if user:  # verifica se o usuario existe no banco de dados, se ele existe vai retornar para o usuario uma mensagem de erro.
            return {"error": "e-mail ja cadastrado!"}, 400

        # Para criar 1 hash no lugar da senha
        user = User()
        user.email = args.email
        user.password = generate_password_hash(args.password, salt_length=10)
        db.session.add(user)

        try:
            db.session.commit()  # aqui faz o insert into no banco de dados
            send_mail(
                "Bem-Vindo(a) Shiny Store",
                user.email,
                "welcome",
                email=user.email,
            )

            return {"message": "Usuario registrado com sucesso!"}, 201

        except Exception as e:
            db.session.rollback()
            logging.critical(str(e))
            return ({"error": "nao foi possivel fazer o registro do usuario."}, 500)


class ForgetPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument("email", required=True,
                            help="o campo e-mail e obrigatorio")
        args = parser.parse_args()

        user = User.query.filter_by(email=args.email).first()
        if not user:
            return {"error": "dados nao encontrados"}, 400

        password_temp = secrets.token_hex(8)
        user.password = generate_password_hash(password_temp)
        db.session.commit()

        send_mail("Suporte - Recuperação de conta",
                  user.email,
                  "forget-password",
                  password_temp=password_temp,
                  )
        return {"message": "e-mail enviado com sucesso!"}
