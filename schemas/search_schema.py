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
    course_title:
        e.g. protein
    course_type:
        possible values: ALL, ACT (activity), COL (colloquium), DIS (discussion),
            FLD (field work), LAB (labratory), LEC (lecture), QIZ (quiz),
            RES (research), SEM (seminar), STU (studio), TUT (tutorial)
    units:
        e.g. 3, 4, VAR (for variable unit classes)
    days:
        e.g. MWF, TuTh, W (courses will include all days specified)
    starts_after:
        possible values: 1:00am through 11:00pm 
    ends_before:
        possible values: 2:00am through 11:00pm
    max_capacity:
        e.g. >50, <20
    full_courses:
        possible values: ANY, SkipFullWaitlist, SkipFull, FullOnly, OverEnrolled
    cancelled_courses:
        possible values: Exclude, Include, Only
    building:
        help: https://www.reg.uci.edu/addl/campus
    """

    term = fields.Str(required=True)
    category = fields.Str(missing="ANY")
    department = fields.Str(missing=" ALL")
    course_number = fields.Str(missing="")
    course_level = fields.Str(missing="ANY")
    course_code = fields.Str(missing="")
    instructor = fields.Str(missing="")
    course_title = fields.Str(missing="")
    course_type = fields.Str(missing="ALL")
    units = fields.Str(missing="")
    days = fields.Str(missing="")
    starts_after = fields.Str(missing="&nbsp;")
    ends_before = fields.Str(missing="&nbsp;")
    max_capacity = fields.Str(missing="")
    full_courses = fields.Str(missing="ANY")
    cancelled_courses = fields.Str(missing="Exclude")
    building = fields.Str(missing="")
    room = fields.Str(missing="")
