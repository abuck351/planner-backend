from flask import request
from flask_restful import Resource
from webargs.flaskparser import parser
import utils.db as db
import utils.messages as msg
from schemas.results_schema import ResultsSchema


class ResultsResource(Resource):
    def post(self):
        args = parser.parse(ResultsSchema, request)
        print(args)
