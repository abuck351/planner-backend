from flask import request
from flask_restful import Resource

import utils.messages as msg
import utils.db as db
from models.departments_model import DepartmentsModel
from websoc.departments_scraper import update_departments


class DepartmentsResource(Resource):
    def get(self):
        try:
            departments = db.find_by(DepartmentsModel)
            return {"depts": [dept.json() for dept in departments]}
        except Exception as e:
            print(e)
            return {"message": msg.internal_server("retrieve", "Departments")}, 500

    def post(self):
        try:
            update_departments()
            return {"message": msg.success("Departments", "updated")}, 200
        except Exception as e:
            print(e)
            return {"message": msg.internal_server("update", "Departments")}, 500
