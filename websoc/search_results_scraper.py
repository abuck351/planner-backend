from typing import Dict, Any

from bs4 import BeautifulSoup
import requests

import utils.db as db
import websoc.settings as websoc
from websoc.utils import parse_year_term
from models.course_model import CourseModel


def _parse_title(text: str) -> str:
    try:
        text_list = text.replace(u"\xa0", u" ").split()
        if "(Prerequisites)" in text_list:
            text_list = text_list[:-1]
        return " ".join(text_list)
    except Exception as e:
        print(e)
        return text


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

    courses = []
    course = {}

    for i, row in enumerate(soup.find_all("tr", {"valign": "top"})):
        cells = row.find_all("td")
        if len(cells) == 1:
            # This row displays the course title (should be the first row found)
            course = {}
            courses.append(course)
            course["title"] = _parse_title(cells[0].text)
            course["sections"] = []
            continue

        section = {}
        for j, cell in enumerate(cells):
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

    headers = ["section_type", "section_name", "meeting_time", "instructor", "building"]
    for header in headers:
        course_data[header] = section.get(header)

    course = CourseModel(**course_data)
    db.save(course)
    return course._id

