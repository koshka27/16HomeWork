from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from data import users, orders, offers
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(50))


class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))


db.create_all()
# print(Order.query.get(1).name)
for user_data in users:
    new_user = User(
        id=user_data["id"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        age=user_data["age"],
        email=user_data["email"],
        role=user_data["role"],
        phone=user_data["phone"],
    )

    db.session.add(new_user)
    db.session.commit()

for order_data in orders:
    new_order = Order(
        id=order_data["id"],
        name=order_data["name"],
        description=order_data["description"],
        start_date=order_data["start_date"],
        end_date=order_data["end_date"],
        address=order_data["address"],
        price=order_data["price"],
        customer_id=order_data["customer_id"],
        executor_id=order_data["executor_id"],
    )

    db.session.add(new_order)
    db.session.commit()

for offer_data in offers:
    new_offer = Offer(
        id=offer_data["id"],
        order_id=offer_data["order_id"],
        executor_id=offer_data["executor_id"],
    )

    db.session.add(new_offer)
    db.session.commit()


@app.route("/users/", methods=['GET', 'POST'])
def get_users_all():
    if request.method == "GET":
        result = []
        for u in Order.query.all():
            result.append(u.to_dict())
        return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["user_data"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )
        db.session.add(new_order)
        db.session.commit()
        return "", 201


@app.route("/users/<int:oid>", methods=['GET', 'PUT', 'DELETE'])
def user(oid: int):
    if request.method == "GET":
        return json.dumps(User.query.get(oid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        u = User.query.get(oid)
        db.session.delete(u)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        user_data = json.loads(request.data)
        u = User.query.get(oid)
        u.first_name = user_data["user_data"]
        u.last_name = user_data["user_data"]
        u.age = user_data["user_data"]
        u.email = user_data["user_data"]
        u.role = user_data["user_data"]
        u.phone = user_data["user_data"]

        db.session.add(u)
        db.session.commit()
        return "", 204


@app.route("/orders", methods=['GET', 'POST'])
def orders():
    if request.method == "GET":
        result = []
        for u in Order.query.all():
            result.append(u.to_dict())
        return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        order_data = json.loads(request.data)
        new_order = Order(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"],
        )
        db.session.add(new_order)
        db.session.commit()
        return "", 201


@app.route("/orders/<int:oid>", methods=['GET', 'PUT', 'DELETE'])
def order(oid: int):
    if request.method == "GET":
        return json.dumps(Order.query.get(oid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        u = Order.query.get(oid)
        db.session.delete(u)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        order_data = json.loads(request.data)
        u = Order.query.get(oid)
        u.name = order_data["order_data"]
        u.description = order_data["order_data"]
        u.start_date = order_data["order_data"]
        u.end_date = order_data["order_data"]
        u.address = order_data["order_data"]
        u.price = order_data["order_data"]
        u.customer_id = order_data["order_data"]
        u.executor_id = order_data["order_data"]

        db.session.add(u)
        db.session.commit()
        return "", 204


@app.route("/offers", methods=['GET', 'POST'])
def get_offers():
    if request.method == "GET":
        result = []
        for u in Offer.query.all():
            res = {
                "id": u.id,
                "order_id": u.order_id,
                "executor_id": u.executor_id,
            }
            result.append(res)
        return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route("/offers/<int:oid>", methods=['GET', 'PUT', 'DELETE'])
def get_offer(oid: int):
    if request.method == "GET":
        return json.dumps(Offer.query.get(oid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        u = Offer.query.get(oid)
        db.session.delete(u)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        offer_data = json.loads(request.data)
        u = Offer.query.get(oid)
        u.order_id = offer_data["offer_data"]
        u.executor_id = offer_data["offer_data"]

        db.session.add(u)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
