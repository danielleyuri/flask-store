from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.extensions import db
from app.models import User, Product, Category, Profile, Order, Item
from slugify import slugify
from wtforms.fields import StringField
from wtforms.validators import Optional
from werkzeug.security import generate_password_hash

class UserModel(ModelView):
    inline_models = [Profile]

    def on_model_change(self, form, model, is_created):
         model.password = generate_password_hash(form.password.data,salt_length= 10)


class ProductModel(ModelView):
    form_extra_fields = {
        "slug": StringField("slug", validators=[Optional()])
    }

    column_searchable_list = ("name", )
    column_sortable_list = ("name", "price", "quantity",)
    column_filters = ("price", "quantity", )

    def on_model_change(self, form, model, is_created):
        model.image = form.image.data.encode()
        if form.slug.data:
            model.slug = form.slug.data
            return

        model.slug = slugify(form.name.data)


class CategoryModel(ModelView):
    form_extra_fields = {
        "slug": StringField("slug", validators=[Optional()])
    }

    def on_model_change(self, form, model, is_created):
        model.slug = slugify(form.name.data)


def init_app(app):
    admin = Admin(app, name="ShinyLuna Store")
    admin.add_view(UserModel(User, db.session))
    admin.add_view(ModelView(Profile, db.session))
    admin.add_view(CategoryModel(Category, db.session))
    admin.add_view(ModelView(Item, db.session))
    admin.add_view(ModelView(Order, db.session))
    admin.add_view(ProductModel(Product, db.session))
