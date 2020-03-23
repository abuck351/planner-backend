from marshmallow import Schema, fields


class CourseInPlanSchema(Schema):
    term = fields.Str(required=True)
    course_code = fields.Str(required=True)
