from typing import Dict, Any

from bs4 import BeautifulSoup
import requests

import websoc.settings as websoc


cell_headers = [
    "code",
    "type",
    "section",
    "units",
    "instructor",
    "time",
    "building",
    "final",
    "max",
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
            course["title"] = cells[0].text  # TODO: Fix the ugly formatting
            course["sections"] = []
            continue

        section = {}
        for j, cell in enumerate(cells):
            section[cell_headers[j]] = cell.text
        course["sections"].append(section)

    return courses

