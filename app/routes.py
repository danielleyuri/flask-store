from flask_restful import Api

from app.resources import auth
from app.resources import category
from app.resources import product
from app.resources import order
from app.resources import user



# Acessar as aplicações acessar o domínio
# O prefixo da rota é o api

def init_app(app):
    api = Api(app, prefix= "/api")

    api.add_resource(auth.Login, "/auth/login")
    api.add_resource(auth.Register, "/auth/register")
    api.add_resource(auth.ForgetPassword, "/auth/forget-password")

    api.add_resource(product.ProductList, "/products")
    api.add_resource(product.ProductGet, "/products/<slug>")

    api.add_resource(category.CategoryList, "/categories")
    api.add_resource(category.CategoryGet, "/categories/<slug>")

    api.add_resource(order.Create, "/order/create")
    api.add_resource(order.Pay, "/order/pay/<reference_id>")
    api.add_resource(order.Notification, "/order/notification")

    api.add_resource(user.Orders, "/user/orders")
    api.add_resource(user.ProfileUpdate, "/user/profile")


