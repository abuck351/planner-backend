from flask import request
from flask_restful import Resource
from webargs.flaskparser import parser

import utils.messages as msg
from websoc.search_results_scraper import scrape
from schemas.search_schema import SearchSchema


def parse_year_term(arg: str):
    year, term = arg.split("-")
    term_translator = {
        "WINTER": "03",
        "SPRING": "14",
        "SUM1": "25",
        "SUM10": "39",
        "SUMCOM": "51",
        "SUM2": "76",
        "FALL": "92",
    }
    return f"{year}-{term_translator[term]}"


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
                data[data_map["term"]] = parse_year_term(arg_value)
                continue

            data[data_map[arg_name]] = arg_value

        return {"results": scrape(data)}
