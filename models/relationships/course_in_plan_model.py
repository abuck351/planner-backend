from typing import Dict

from utils.db import db


class CourseInPlanModel(db.Model):
    __tablename__ = "CoursesInPlans"

    plan_id = db.Column(db.Integer, db.ForeignKey("Plans._id"), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("Courses._id"), primary_key=True)

    def json(self) -> Dict:
        return {"plan_id": self.plan_id, "course_id": self.course_id}
