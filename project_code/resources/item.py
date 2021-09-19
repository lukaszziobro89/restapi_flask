import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="The field cannot left blank!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"An item {name} already exists."}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            Item.insert(item)
        except:
            return {"message": "An error occur when inserting"}, 500

        return item, 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {"message": f"Item {name} does not exists"}
        else:
            connection = sqlite3.connect('project_code/data.db')
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name = ?"
            cursor.execute(query, (name,))

            connection.commit()
            connection.close()

            return {"message": f"Item {name} deleted"}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                ItemModel.insert(updated_item)
            except:
                return {"message": "An error occurred when inserting an item"}, 500
        else:
            try:
                ItemModel.update(updated_item)
            except:
                return {"message": "An error occurred when update an item"}, 500
        return updated_item


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('project_code/data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}
