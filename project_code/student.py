from flask_restful import Resource


class Student(Resource):

    def get(self, name):
        return {"student": name}
