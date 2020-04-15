import traceback

from flask import request
from flask_restful import Resource
from webargs.flaskparser import parser

import utils.db as db
import utils.messages as msg
from models.plan_model import PlanModel


class PlanResource(Resource):
    def get(self, name):
        term = request.args.get("term")

        try:
            if term:
                plans = db.find_by(PlanModel, name=name, term=term).all()
            else:
                plans = db.find_by(PlanModel, name=name).all()
        except:
            traceback.print_exc()
            return {"message": msg.internal_server("retrieve", "Plan")}, 500

        if plans:
            return {"plans": [plan.json() for plan in plans]}
        else:
            identifier = (name, term) if term else name
            return {"message": msg.not_found("Plan", identifier)}, 404

    def post(self, name):
        term = request.args.get("term")
        if term is None:
            return {"message": msg.bad_parameters("term")}, 400

        plan = db.find_by(PlanModel, name=name, term=term).first()
        if plan:
            return {"message": f"A plan named {name} for {term} already exists"}, 400

        plan = PlanModel(name=name, term=term)
        try:
            db.save(plan)
        except:
            traceback.print_exc()
            return {"message": msg.internal_server("save", "PlanModel")}, 500

        return {"message": msg.success("Plan", "created"), "plan": plan.json()}, 201
