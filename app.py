import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv

from utils.db import db

# Resource Imports
from resources.search_resource import SearchResource
from resources.departments_resource import DepartmentsResource
from resources.plan_resource import PlanResource
from resources.course_in_plan_resource import CourseInPlanResource

# App Settings
load_dotenv(verbose=True)
DB_URI = os.getenv("DB_URI")
PLANNER_SECRET_KEY = os.getenv("PLANNER_SECRET_KEY")

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.secret_key = PLANNER_SECRET_KEY
CORS(app)


@app.before_first_request
def create_tables():
    db.create_all()


api = Api(app)
api.add_resource(SearchResource, "/api/search")
api.add_resource(DepartmentsResource, "/api/depts")
api.add_resource(PlanResource, "/api/plans/<string:name>")
# TODO: Add CourseInPlanResource

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
