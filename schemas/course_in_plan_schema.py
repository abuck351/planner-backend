from marshmallow import Schema, fields


class CourseInPlanSchema(Schema):
    plan_id = fields.Str(required=True)
    course_code = fields.Str(required=True)
