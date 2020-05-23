from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    
    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
        
#create the product schema 
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')
    
#initialize the schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route('/product',methods=['POST'])
def add_product():
    product = request.get_json()
    new_product = Product(product['name'], product['description'], product['price'], product['qty'])
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)


@app.route('/product/<p_id>/', methods=['DELETE'])
def delete_product(p_id):
    product = Product.query.filter_by(id=p_id).first()
    print(product)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message':'Product deleted!'})

@app.route('/product/<p_id>/',methods=['PUT'])
def update_product(p_id):
    product = Product.query.filter_by(id=p_id).first()
    update = request.get_json()
    product.name = update['name']
    product.description = update['description']
    product.price = update['price']
    product.qty = update['qty']
    db.session.commit()
    return jsonify({'message':'Product Updated!'})
    return product_schema.jsonify(product)

@app.route('/product', methods=['GET'])
def get_all_product():
    products = Product.query.all()
    products_list = []
    for product in products:
        products_data = {}
        products_data['id'] = product.id
        products_data['name'] = product.name
        products_data['description'] = product.description
        products_data['price'] = product.price
        products_data['qty'] = product.qty
        products_list.append(products_data)
    return jsonify({'products': products_list})
    
@app.route('/product/<p_id>/', methods=['GET'])
def get_one_product(p_id):
    product = Product.query.filter_by(id=p_id).first()
    product_data = {}
    product_data['id'] = product.id
    product_data['name'] = product.name
    product_data['description'] = product.description
    product_data['price'] = product.price
    product_data['qty'] = product.qty
    return jsonify({'product': product_data})

@app.route('/test', methods=['GET'])
def test():
    fetch = Product.query.all()
    result = products_schema.dump(fetch)
    return jsonify(result.data)

@app.route('/debug')
def debug():
    pass

if __name__ == "__main__":
    app.run(debug=True)