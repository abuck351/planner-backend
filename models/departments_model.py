from utils.db import db


class DepartmentsModel(db.Model):
    __tablename__ = "Departments"

    value = db.Column(db.String, primary_key=True)
    text = db.Column(db.String, nullable=False)

    def __str__(self) -> str:
        return f"{self.value}: {self.text}"
