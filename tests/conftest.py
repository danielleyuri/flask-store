from app import create_app
from pytest import fixture
from app.extensions import db
from app.models import Product, Category 
from slugify import slugify


@fixture
def app():
     app = create_app()
     app.testing = True 
     return app


@fixture
def create_database(app):
     with app.app_cantext:
          db.create_all()

          yield db

          db.session.remove()
          db.drop_all()


@fixture(autouse=True)
def makedb(create_databe):
     p = Product()
     p.name = "Xbox One Series X"
     p.slaug = slugify(p.name)
     p.price = 299.90
     p.description = "console da microsoft"
     p.image = b"image.jpg"
     p.quantity = 20

     c = Category()
     c.name = "games"
     c.slug = slugify(c.name)

     c2 = Category
     c2.name = "informatica"
     c2.slug = slugify(c2.name)


     db.session.add(p)
     db.session.add(c)
     db.session.add(c2)
     
     db.session.commit()