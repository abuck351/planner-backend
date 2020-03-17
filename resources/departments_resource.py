from flask import request
from flask_restful import Resource
import utils.db as db
from websoc.scrape_departments import update_departments
import utils.messages as msg
from schemas.results_schema import ResultsSchema


class DepartmentsResource(Resource):
    def get(self):
        pass

    def post(self):
        try:
            update_departments()
            return {"message": msg.success("Departments", "updated")}
        except Exception as e:
            print(e)
            return {"message": msg.internal_server("update", "Departments")}
