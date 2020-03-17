from flask import request
from webargs.flaskparser import parser
from flask_restful import Resource
import utils.messages as msg
import websoc.search_parsers
from websoc.scrape_search_results import scrape

# Data
import utils.db as db
from schemas.search_schema import SearchSchema


class SearchResource(Resource):
    def post(self):
        args = parser.parse(SearchSchema, request)

        data = {}
        data["YearTerm"] = websoc.search_parsers.year_term(args["term"])
        data["ShowComments"] = False
        data["ShowFinals"] = True
        data["Breadth"] = args["category"]
        data["Dept"] = args["department"]
        data["CourseNum"] = ""
        data["Division"] = "ANY"
        data["CourseCodes"] = ""
        data["InstrName"] = ""
        data["CourseTitle"] = ""
        data["ClassType"] = ""
        data["Units"] = ""
        data["Days"] = ""
        data["StartTime"] = "&nbsp;"
        data["EndTime"] = "&nbsp;"
        data["MaxCap"] = ""
        data["FullCourses"] = "ANY"
        data["FontSize"] = "100"
        data["CancelledCourses"] = "Exclude"
        data["Bldg"] = ""
        data["Room"] = ""

        print(data)
        return {"results": scrape(data)}
