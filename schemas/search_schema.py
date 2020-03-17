from marshmallow import Schema, fields


class SearchSchema(Schema):
    """
    term:
        format: YYYY-TERM
        TERM: WINTER, SPRING, SUM1, SUM10, SUMCOM, SUM2, FALL
        e.g. 2020-FALL
    category:
        possible values: ANY, GE-1A, GE-1B, GE-2, GE-3, GE-4, 
            GE-5A, GE-5B, GE-6, GE-7, GE-8
    department:
        These values are scraped from WebSoc and stored in the database
        e.g. ANATOMY
    course_number:
        e.g. H2A, 5, 10-20 (multiple entries OK)
    course_level:
        possible values: ANY, LOWER, UPPER, GRAD
    course_code:
        e.g. 14200, 29000-29100
    instructor:
        e.g. smith
    """

    term = fields.Str(required=True)
    category = fields.Str()
    department = fields.Str()
    # course_number = fields.Str()
    # course_level = fields.Str()
    # course_code = fields.Str()
    # instructor = fields.Str()
    # TODO: Add the other websoc fields later
