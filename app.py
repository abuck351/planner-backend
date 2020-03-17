from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from utils.db import db
import settings

# Resource Imports
from resources.search_resource import SearchResource
from resources.departments_resource import DepartmentsResource

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URI
app.secret_key = settings.PLANNER_SECRET_KEY
CORS(app)


@app.before_first_request
def create_tables():
    db.create_all()


api = Api(app)
# api.add_resource(<>, "/my/route")
api.add_resource(SearchResource, "/api/search")
api.add_resource(DepartmentsResource, "/api/depts")


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
