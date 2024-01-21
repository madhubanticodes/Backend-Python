from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# In-memory storage for products and orders
products = {}
orders = {}


# Product resource
class ProductResource(Resource):
    def get(self, product_id):
        if product_id in products:
            return products[product_id]
        else:
            return {"error": "Product not found"}, 404

    def delete(self, product_id):
        if product_id in products:
            del products[product_id]
            return {"message": "Product deleted successfully"}
        else:
            return {"error": "Product not found"}, 404


class ProductsResource(Resource):
    def get(self):
        return products

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True, help="Product name is required")
        parser.add_argument("price", type=float, required=True, help="Product price is required")
        args = parser.parse_args()

        product_id = len(products) + 1
        product = {"id": product_id, "name": args["name"], "price": args["price"]}
        products[product_id] = product

        return product, 201


# Order resource
class OrderResource(Resource):
    def get(self, order_id):
        if order_id in orders:
            return orders[order_id]
        else:
            return {"error": "Order not found"}, 404


class OrdersResource(Resource):
    def get(self):
        return orders

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("product_id", type=int, required=True, help="Product ID is required")
        parser.add_argument("quantity", type=int, required=True, help="Quantity is required")
        args = parser.parse_args()

        product_id = args["product_id"]
        quantity = args["quantity"]

        if product_id not in products:
            return {"error": "Product not found"}, 404

        if product_id not in orders:
            orders[product_id] = {"product_id": product_id, "quantity": quantity}
        else:
            orders[product_id]["quantity"] += quantity

        return orders[product_id], 201


# Add resources to API
api.add_resource(ProductResource, '/products/<int:product_id>')
api.add_resource(ProductsResource, '/products')
api.add_resource(OrderResource, '/orders/<int:order_id>')
api.add_resource(OrdersResource, '/orders')

if __name__ == '__main__':
    app.run(debug=True)
