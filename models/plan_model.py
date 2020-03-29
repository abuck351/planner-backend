import traceback
from typing import Dict

from utils.db import db, find_by
from models.course_model import CourseModel
from models.relationships.course_in_plan_model import CourseInPlanModel


class PlanModel(db.Model):
    __tablename__ = "Plans"

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    term = db.Column(db.String, nullable=False)

    __table_args__ = (db.UniqueConstraint("name", "term"),)

    def json(self) -> Dict:
        courses = []
        try:
            courses_in_plan = find_by(CourseInPlanModel, plan_id=self._id).all()
        except Exception as e:
            traceback.print_exc()
        else:
            for course_in_plan in courses_in_plan:
                try:
                    course = find_by(CourseModel, _id=course_in_plan.course_id).first()
                    courses.append(course.json())
                except Exception as e:
                    traceback.print_exc()

        return {
            "_id": self._id,
            "name": self.name,
            "term": self.term,
            "courses": courses,
        }
