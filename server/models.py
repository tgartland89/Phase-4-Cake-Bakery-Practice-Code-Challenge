from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here
class Cake(db.Model):
    __tablename__ = 'cakes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Using backref
    cake_bakeries = db.relationship('CakeBakery', backref='cake')

    # Using association_proxy to access bakeries directly
    bakeries = association_proxy('cake_bakeries', 'bakery')


class Bakery(db.Model):
    __tablename__ = 'bakeries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    
    # Using backref
    cake_bakeries = db.relationship('CakeBakery', backref='bakery')

    # Using association_proxy to access cakes directly
    cakes = association_proxy('cake_bakeries', 'cake')


class CakeBakery(db.Model):
    __tablename__ = 'cake_bakeries'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    cake_id = db.Column(db.Integer, db.ForeignKey('cakes.id'))
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))


    @validates('price')
    def validate_price(self, key, price):
        if not isinstance(price, int):
            raise ValueError('Price must be an integer.')
        if price < 1 or price > 1000:
            raise ValueError('Price must be between 1 and 1000.')
        return price
    