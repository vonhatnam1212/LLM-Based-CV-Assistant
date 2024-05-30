from flask import Flask
from flask_restful import reqparse
from flask_restful import Api, Resource

from query_CV import user_query


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(HelloWorld, "/")
    api.add_resource(TransformData, "/query_CV")

    return app


class HelloWorld(Resource):
    def get(self):
        return {"data": "Hello, my name is VNN"}


class GetData(Resource):
    def __init__(self):
        query_args = reqparse.RequestParser()
        query_args.add_argument(
            "user_input", type=str, required=True, help="user input missing"
        )
        query_args.add_argument(
            "model", type=str, required=True, help="model missing"
        )
        self.query_args = query_args


class TransformData(GetData):
    def post(self):
        args = self.query_args.parse_args()
        
        try:
            query, token, file_name_document = user_query(args["user_input"])
            print(query,token)
            result = {
                "code": 200,
                "message": "success",
                "result": query["result"],
                "cost": token.total_cost,
                "token": token.total_tokens,
                "list_docs": file_name_document,
            }
        except:
            result = {
                "code": 400,
                "message": "error",
            }
        return result


app = create_app()

if __name__ == "__main__":
    create_app().run()
