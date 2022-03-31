import logging
from random import getrandbits
import datetime 

from app.extensions import db
from app.models import Item, Order, Product
from app.schemas import order_fields


from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, marshal, reqparse
from app.services.picpay import picpay
from flask import current_app, request
from app.enums import EStatus


class Create(Resource):
    @jwt_required  # Garante que o cliente so vai gerar o pedido se estiver logado!
    def post(self):
        current_user = get_jwt_identity()       # Vai encontrar o cliente que esta logado.

        parser = reqparse.RequestParser()
        parser.add_argument("product_id", type=int,
                            required=True, help="product_id obrigatório")
        parser.add_argument("quantity", type=int,
                            required=True, help="quantity obrigatorio")

        args = parser.parse_args()

        product = Product.query.get(args.product_id)
        if not product:
            return {"error": "produto nao encontrado em nossa base"}, 400

        if args.quantity > product.quantity:
            return {"error": "não possuimos essa quantidade"}, 400

        try:
            order = Order()
            order.reference_id = f"FLS-{getrandbits(16)}"
            db.session.add(order)
            db.session.commit()

            item = Item()
            item.order_id = order.id
            item.product_id = product.id
            item.user_id = current_user["id"]
            item.quantity = args.quatity
            item.price = product.price * args.quantity
            db.session.add(item)
            db.session.commit()
            return marshal(order, order_fields, "order")
        except Exception as e:
            logging.critical(str(e))
            db.session.rollback()
            return {"error": "não foi possivel criar o seu pedido"}, 500


class Pay(Resource):
    @jwt_required
    def get(self, reference_id):
        order = Order.query.filter_by(reference_id=reference_id).first()
        if not order:
            return{"error":"pedido não existe!"}, 400

        expires = datetime.datetime.now() + datetime.timedelta(days=3)

        if not order.item.user.profile:
            return {"error":"Voce precisa atualizar o seu perfil antes de continuar."}


        response = picpay.payment(
            {
                "referenceId": order.reference_id,
                "callbackUrl": current_app.config["PICPAY_CALLBACK_URL"],
                "returnUrl": current_app.config["PICPAY_RETURN_URL"],
                "value": order.item.price,
                "expiresAt": expires.isoformat(),
                "buyer": {
                    "firstName": order.item.user.profile.first_name,
                    "lastName": order.item.user.profile.last_name,
                    "document": order.item.user.profile.document,
                    "email": order.item.user.email,
                    "phone": order.item.user.profile.phone,
                },
            }
        )

        return response.json()

class Notification(Resource):
    pass
