import json, os
from QuanLyNhaSach import app, db
from QuanLyNhaSach.models import User, UserRole, Category, Product, OrderDetails, Orders
from sqlalchemy import func
import hashlib


def load_categories():
    return Category.query.all()


def load_products(cate_id=None, kw=None):
    products = Product.query.filter(Product.active.__eq__(True))

    if cate_id:
        products = products.query.filter(Product.category_id.__eq__(cate_id))

    if kw:
        products = products.query.filter(Product.name.contains(kw))

    return products


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.name.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def check_role(user):
    if UserRole.USER == user.user_role:
        return True


def category_stats():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
                            .join(Product, Category.id.__eq__(Product.category_id), isouter=True)\
                            .group_by(Category.id, Category.name).all()


def product_stats(kw=None, from_date=None, to_date=None):
    #theloaisach, doanhthu, soluotthue, tyle
    p = db.session.query(Product.category_id, Category.name,
                         )\
                    .join(Category, Category.id.__eq__(Product.category_id), isouter=True)\
                    .group_by(Product.category_id, Category.name)

    return p.all()


def sales_report(kw=None, from_date=None, to_date=None):
    #tensach, theloai, soluong, tyle
    s = db.session.query(Product.id, Product.name, Product.category_id, OrderDetails.quantity)\
                    .join(OrderDetails, OrderDetails.products_id.__eq__(Product.id), isouter=True)\
                    .group_by(Product.id, Product.name, Product.category_id)

    return s.all()


def add_user(name, username, password, **kwargs):
    new_user = User(name=name.strip(),
                    username=username.strip(),
                    password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()),
                    email=kwargs.get('email'),
                    avatar=kwargs.get('avatar'))

    db.session.add(new_user)
    db.session.commit()