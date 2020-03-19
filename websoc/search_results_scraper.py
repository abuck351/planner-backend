from typing import Dict, Any

from bs4 import BeautifulSoup
import requests

import websoc.settings as websoc


def parse_title(text: str) -> str:
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
            course["title"] = parse_title(cells[0].text)
            course["sections"] = []
            continue

        section = {}
        for j, cell in enumerate(cells):
            section[cell_headers[j]] = cell.text

        course["sections"].append(section)

    return courses

