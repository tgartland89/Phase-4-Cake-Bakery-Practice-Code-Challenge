from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Cake, Bakery, CakeBakery

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/bakery', methods=['POST'])
def create_bakery():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')

    if not name or not address:
        return jsonify({'error': 'Name and address are required fields.'}), 400

    bakery = Bakery(name=name, address=address)
    db.session.add(bakery)
    db.session.commit()

    return jsonify({'message': 'Bakery created successfully.'}), 201

@app.route('/cake', methods=['POST'])
def create_cake():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({'error': 'Name and description are required fields.'}), 400

    cake = Cake(name=name, description=description)
    db.session.add(cake)
    db.session.commit()

    return jsonify({'message': 'Cake created successfully.'}), 201

@app.route('/cake_bakery', methods=['POST'])
def create_cake_bakery():
    data = request.get_json()
    price = data.get('price')
    cake_id = data.get('cake_id')
    bakery_id = data.get('bakery_id')

    # Validate the input
    if not (price and cake_id and bakery_id):
        return jsonify({'error': 'Price, cake_id, and bakery_id are required fields.'}), 400

    # Find the cake and bakery by their IDs
    cake = Cake.query.get(cake_id)
    bakery = Bakery.query.get(bakery_id)

    # Check if the cake and bakery exist
    if not (cake and bakery):
        return jsonify({'error': 'Cake or bakery not found.'}), 404

    # Create and save the cake_bakery
    cake_bakery = CakeBakery(price=price, cake=cake, bakery=bakery)
    db.session.add(cake_bakery)
    db.session.commit()

    # Prepare the response data
    response_data = {
        'cake_id': cake_bakery.cake_id,
        'bakery_id': cake_bakery.bakery_id,
        'price': cake_bakery.price
    }

    return jsonify(response_data), 201



if __name__ == '__main__':
    app.run(port=3000, debug=True)
