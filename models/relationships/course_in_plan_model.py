from typing import Dict

from utils.db import db


class CourseInPlanModel(db.Model):
    __tablename__ = "CoursesInPlans"

    _id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey("Plans._id"))
    course_id = db.Column(db.Integer, db.ForeignKey("Courses._id"))

    __table_args__ = (db.UniqueConstraint("plan_id", "course_id"),)

    def json(self) -> Dict:
        return {"plan_id": self.plan_id, "course_id": self.course_id}
