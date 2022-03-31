from flask_restful import Resource, marshal, reqparse
from app.models import User, Profile
from app.schemas import user_items_fields, profile_fields

from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
import logging


class ProfileUpdate(Resource):
    @jwt_required
    def put(self):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument("first_name", required=True,
                            help="campo obrigatório")
        parser.add_argument("last_name", required=True,
                            help="campo obrigatório")
        parser.add_argument("document", required=True,
                            help="campo obrigatório")
        parser.add_argument("phone", required=True, help="campo obrigatório")
        args = parser.parse_args(strict=True)

        current_user = get_jwt_identity()

        user = User.query.filter_by(id=current_user["id"]).first()
        if not user.profile:
            user.profile = Profile()

        user.profile.first_name = args.first_name
        user.profile.last_name = args.last_name
        user.profile.document = args.document
        user.profile.phone = args.phone

        try:
            db.session.commit()
            return marshal(user.profile, profile_fields, "profile")
        except Exception as e:
            logging.critical(str(e))
            db.session.rollback()
            return {"error": "nao foi possivel atualizar o seu perfil, por favor tente mais tarde"}, 500


class Orders(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.get(current_user["id"])
        return marshal(user.items, user_items_fields)
