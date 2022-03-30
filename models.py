from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from QuanLyNhaSach import db
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    MANAGE = 3
    EMPLOYEE = 4


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100))
    order = relationship('Orders', backref='users', lazy=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.username


class Product(db.Model):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    images = Column(String(100))
    price = Column(Float, nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    order_details = relationship('OrderDetails', backref='products', lazy=True)


    def __str__(self):
        return self.name


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class OrderDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Float, nullable=False)
    products_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)

    def __str__(self):
        return self.name


class Orders(db.Model):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    order_details = relationship('OrderDetails', backref='orders', lazy=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    db.create_all()

    # c1 = Category(name="VAN HOC")
    # c2 = Category(name="GIAO KHOA - THAM KHAO")
    # c3 = Category(name="SACH THIEU NHI")
    #
    # db.session.add(c1)
    # db.session.add(c2)
    # db.session.add(c3)
    #
    # db.session.commit()

    # products = [{
    #      "id": 1,
    #      "name": "Nha Gia Kim",
    #      "description": "Tac gia: Paulo Coelho, Nguoi dich: Le Chu Cau, NXB: NXB Hoi Nha Van, Nam XB: 2020",
    #      "images": "images/nhagiakim.png",
    #      "price": "79000",
    #      "create_date": "01/05/2020",
    #      "active": "True",
    #      "category_id": "1"
    #     },{
    #      "id": 2,
    #      "name": "365 Ki Quan The Gioi",
    #      "description": "Tac gia: OM Books, Nguoi dich: Nhom Soc Xanh, NXB: NXB The Gioi,Nam XB: 2019",
    #      "images": "images/365kiquanthegioi.png",
    #      "price": "154000",
    #      "create_date": "01/02/2019",
    #      "active": "True",
    #      "category_id": "3"
    #     },{
    #      "id": 3,
    #      "name": "Hoa Hoc 10",
    #      "description": "Tac gia: Bo Giao Duc va Dao Tao, NXB: NXB Giao Duc Viet Nam, Nam XB: 2021",
    #      "images": "images/hoahoc10.png",
    #      "price": "7000",
    #      "create_date": "01/01/2021",
    #      "active": "True",
    #      "category_id": "2"
    #     }]
    # for p in products:
    #     pro = Product(name=p['name'], price=p['price'], images=p['images'],
    #                   description=p['description'], category_id=p['category_id'])
    #     db.session.add(pro)
    #
    # db.session.commit()





