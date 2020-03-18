from flask import request
from webargs.flaskparser import parser
from flask_restful import Resource
import utils.messages as msg
import websoc.search_parsers
from websoc.scrape_search_results import scrape

# Data
import utils.db as db
from schemas.search_schema import SearchSchema


data_map = {
    "term": "YearTerm",
    "category": "Breadth",
    "department": "Dept",
    "course_number": "CourseNum",
    "course_level": "Division",
    "course_code": "CourseCodes",
    "instructor": "InstrName",
    "course_title": "CourseTitle",
    "course_type": "ClassType",
    "units": "Units",
    "days": "Days",
    "starts_after": "StartTime",
    "ends_before": "EndTime",
    "max_capacity": "MaxCap",
    "full_courses": "FullCourses",
    "cancelled_courses": "CancelledCourses",
    "building": "Bldg",
    "room": "Room",
}


class SearchResource(Resource):
    def post(self):
        args = parser.parse(SearchSchema, request)

        data = {}
        data["ShowComments"] = False
        data["ShowFinals"] = True
        data["FontSize"] = "100"

        for arg_name, arg_value in args.items():
            if arg_name == "term":
                data["term"] = websoc.search_parsers.year_term(arg_value)
                continue
            data[data_map[arg_name]] = arg_value

        data["YearTerm"] = websoc.search_parsers.year_term(args["term"])

        print(data)
        return {"results": scrape(data)}
