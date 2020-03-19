from typing import Dict

from utils.db import db


class CourseInPlanModel(db.Model):
    __tablename__ = "CoursesInPlans"

    plan_id = db.Column(db.Integer, db.ForeignKey("Plans._id"), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("Courses._id", primary_key=True))

    # Check if a course with term & code already is in Courses table
    # If it is already there, get its _id,
    #   then store plan_id, and course_id in CourseInPlan table
    # Else if the course does NOT exist,
    #   then create the course in Cthe Courses table by scraping WebSoc
    #   and finally store plan_id and the newly created course_id in the
    #   CourseInPlan table

    def json(self) -> Dict:
        # TODO: Finish this
        return {}
