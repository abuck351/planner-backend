import traceback

from flask import request
from flask_restful import Resource
from webargs.flaskparser import parser

import utils.db as db
import utils.messages as msg
from models.relationships.course_in_plan_model import CourseInPlanModel
from schemas.course_in_plan_schema import CourseInPlanSchema
from models.plan_model import PlanModel
from models.course_model import CourseModel
from websoc.search_results_scraper import save_to_db


def _get_plan_id(plan_name: str, term: str) -> int:
    plan = db.find_by(PlanModel, name=plan_name, term=term).first()
    if plan:
        return plan._id
    return -1


def _get_course_id(term: str, course_code: str) -> int:
    course = db.find_by(CourseModel, term=term, code=course_code).first()
    if course:
        return course._id
    return save_to_db(term, course_code)


class CourseInPlanResource(Resource):
    def post(self, plan_name):
        args = parser.parse(CourseInPlanSchema, request)

        # Get the plan_id
        try:
            plan_id = _get_plan_id(plan_name, args["term"])
            if plan_id == -1:
                return (
                    {"message": msg.not_found("Plan", (plan_name, args["term"]))},
                    404,
                )
        except Exception as e:
            traceback.print_exc()
            return {"message": msg.internal_server("retrieve", "Plan")}, 500

        # Get the course_id
        try:
            course_id = _get_course_id(args["term"], args["course_code"])
            if course_id == -1:
                return (
                    {
                        "message": msg.not_found(
                            "Course", (args["term"], args["course_code"])
                        )
                    },
                    404,
                )
        except Exception as e:
            traceback.print_exc()
            return {"message": msg.internal_server("retrieve", "Course")}, 500

        # Make sure the course hasn't already been added to the plan
        if db.find_by(CourseInPlanModel, plan_id=plan_id, course_id=course_id).first():
            return {"message": "Course already added"}

        # Save the plan_id and course_id in the CoursesInPlans table
        course_in_plan = CourseInPlanModel(plan_id=plan_id, course_id=course_id)
        try:
            db.save(course_in_plan)
            return course_in_plan.json()
        except Exception as e:
            traceback.print_exc()
            return {"message": msg.internal_server("save", "Course")}, 500

    def delete(self, plan_name):
        pass
