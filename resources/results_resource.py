from flask import request
from webargs.flaskparser import parser
from flask_restful import Resource
import utils.messages as msg

# Data
import utils.db as db
from schemas.results_schema import ResultsSchema


class ResultsResource(Resource):
    def post(self):
        args = parser.parse(ResultsSchema, request)
        print(args)
