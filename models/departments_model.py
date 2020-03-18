from typing import Dict

from utils.db import db


class DepartmentsModel(db.Model):
    __tablename__ = "Departments"

    _id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    def json(self) -> Dict:
        return {"_id": self._id, "code": self.value, "name": self.text}

    def __str__(self) -> str:
        return f"{self._id}, {self.code}, {self.name}"
