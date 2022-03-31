from itertools import product
from app.models import Product
from flask_restful import Resource, marshal_with, marshal
from app.schemas import product_fields 

#Serializando Modelos
class ProductList(Resource):  

     @marshal_with(product_fields, "products")
     def get(self):
          products = Product.query.all() # select * from products 
          return products

class ProductGet(Resource):

     def get(self, slug):
          product = Product.query.filter_by(slug=slug).first()
          if not product:
               return {"error":"produto não encontrado"}, 400

          return marshal(product, product_fields)

