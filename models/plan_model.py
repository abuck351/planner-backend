from typing import Dict

from utils.db import db


class PlanModel(db.Model):
    __tablename__ = "Plans"

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    __table_args__ = db.UniqueConstraint("name")

    def json(self) -> Dict:
        return {"_id": self._id, "name": self.name}
