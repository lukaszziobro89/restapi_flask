import logging

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, ItemList
from security import identity, authenticate
from student import Student

from resources.user import UserRegister


def create_app():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M"
    )

    app = Flask(__name__)
    app.secret_key = 'secret_key'
    api = Api(app)

    jwt = JWT(app, authenticate, identity)

    api.add_resource(Student, "/student/<string:name>")
    api.add_resource(Item, "/item/<string:name>")
    api.add_resource(ItemList, "/items")
    api.add_resource(UserRegister, "/register")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=True)
