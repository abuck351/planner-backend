from typing import Dict, Any
import traceback

from bs4 import BeautifulSoup
import requests

import utils.db as db
import websoc.settings as websoc
from websoc.utils import parse_year_term
from models.course_model import CourseModel


restriction_map = {
    "A": "Prerequisite required",
    "B": "Authorization required",
    "I": "Seniors only",
    "K": "Graduate only",
    "L": "Major only",
    "N": "School major only",
    "S": "Satisfactory/unsatisfactory only"
}


def _parse_title(text: str) -> str:
    try:
        text_list = text.replace(u"\xa0", u" ").split()
        if "(Prerequisites)" in text_list:
            text_list = text_list[:-1]
        return " ".join(text_list)
    except:
        traceback.print_exc()
        return text


def _parse_enrolled(text: str) -> int:
    try:
        if "/" in text:
            return int(text.split("/")[0].strip())
        else:
            return int(text)
    except ValueError as e:
        traceback.print_exc()
        return 0


def _parse_max_capacity(text: str) -> int:
    try:
        return int(text)
    except ValueError as e:
        traceback.print_exc()
        return 1


def _parse_meeting_time(text: str) -> (str, str, str, str):
    """
    Returns (days, start_time, end_time, time_display)
    """
    # Clean up text and split it into days and time
    try:
        if "TBA" in text:
            return "TBA", None, None, "TBA"

        if "\n" in text:
            text = text.split("\n")[0]
        days_and_time = ' '.join(text.split()).split()

        days = days_and_time[0]
        
        time = ''.join(days_and_time[1:]).split('-')
        time_display = f"{time[0]}-{time[1]}"
        pm = 'p' in time[1]
        if pm:
            time[1] = time[1][:-1]
            
        # Start time
        start_hour, start_minutes = time[0].split(':')
        start_hour = int(start_hour)
        if pm and start_hour < 10:
            start_hour += 12
        start_time = f"{start_hour}:{start_minutes}:00"
        
        # End time
        end_hour, end_minutes = time[1].split(':')
        end_hour = int(end_hour)
        if pm and end_hour <= 11:
            end_hour += 12
        end_time = f"{end_hour}:{end_minutes}:00"
        
        return days, start_time, end_time, time_display
    except Exception:
        traceback.print_exc()
        return "TBA", None, None, "TBA"


def _parse_restrictions(text: str) -> str:
    restriction_codes = text.split(" and ")
    restrictions = []
    for restriction_code in restriction_codes:
        restriction = restriction_map.get(restriction_code)
        if restriction:
            restrictions.append(restriction)
    if restrictions is None or len(restrictions) == 0:
        return None
    return ", ".join(restrictions)

cell_headers = [
    "code",
    "section_type",
    "section_name",
    "units",
    "instructor",
    "meeting_time",
    "building",
    "final_time",
    "max_capacity",
    "enrolled",
    "waitlist",
    "requests",
    "new_only",
    "restrictions",
    "textbooks",
    "website",
    "status",
]


def scrape(search_data: Dict[str, Any]) -> [Dict[str, str]]:
    source = requests.post(
        websoc.URL,
        headers={
            "User-Agent": websoc.USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data=search_data,
    ).content
    soup = BeautifulSoup(source, "lxml")

    courses_count = 0
    courses = []
    course = {}

    for i, row in enumerate(soup.find_all("tr", {"valign": "top"})):
        cells = row.find_all("td")
        if len(cells) == 1:
            # This row displays the course title (should be the first row found)
            course = {}
            courses.append(course)
            courses_count += 1
            course["count"] = courses_count
            course["title"] = _parse_title(cells[0].text)
            course["sections"] = []
            continue

        section = {}
        for j, cell in enumerate(cells):

            # TODO: I could do something more elegant where the "parsing"
            #       functions are also stored in the cell_headers dictionary
            if cell_headers[j] == "enrolled":
                section["enrolled"] = _parse_enrolled(cell.text)
            elif cell_headers[j] == "max_capacity":
                section["max_capacity"] = _parse_max_capacity(cell.text)
            elif cell_headers[j] == "meeting_time":
                days, start_time, end_time, time_display = _parse_meeting_time(cell.text)
                section["days"] = days
                section["start_time"] = start_time
                section["end_time"] = end_time
                section["time_display"] = time_display
            elif cell_headers[j] == "restrictions":
                section["restrictions"] = _parse_restrictions(cell.text)
            else:
                section[cell_headers[j]] = cell.text

        course["sections"].append(section)

    return courses


def save_to_db(term: str, course_code: str) -> int:
    # TODO: It would probably be usefull to create a dictionary with
    #       default data values
    search_data = {
        "ShowComments": False,
        "ShowFinals": True,
        "FontSize": "100",
        "YearTerm": parse_year_term(term),
        "Breadth": "ANY",
        "Dept": " ALL",
        "CourseNum": "",
        "Division": "ANY",
        "CourseCodes": course_code,
        "InstrName": "",
        "CourseTitle": "",
        "ClassType": "ALL",
        "Units": "",
        "Days": "",
        "StartTime": "&nbsp;",
        "EndTime": "&nbsp;",
        "MaxCap": "",
        "FullCourses": "ANY",
        "CancelledCourses": "Exclude",
        "Bldg": "",
        "Room": "",
    }

    scraped_courses = scrape(search_data)
    if not scraped_courses:
        return -1  # Did not find any courses given term and course_code
    scraped_course = scraped_courses[0]
    course_data = {
        "term": term,
        "code": course_code,
        "title": scraped_course.get("title"),
    }

    sections = scraped_course.get("sections")
    if not sections:
        return -1  # The course doesn't have any sections
    section = sections[0]

    for header in ["section_type", "section_name", "days", "start_time", "end_time", "instructor", "building", "restrictions"]:
        course_data[header] = section.get(header)

    course = CourseModel(**course_data)
    db.save(course)
    return course._id
