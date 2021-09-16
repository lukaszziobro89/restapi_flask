import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


items = []


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="The field cannot left blank!")

    # @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('project_code/data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items where name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        else:
            return {'message': 'Item not found'}, 400

    @jwt_required()
    def post(self, name):

        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {f"An item {name} already exists."}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}
