from flask import request
from flask_restful import Resource
from webargs.flaskparser import parser

import utils.messages as msg
from schemas.course_in_plan_schema import CourseInPlanSchema


class CourseInPlanResource(Resource):
    pass
