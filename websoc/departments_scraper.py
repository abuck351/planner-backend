from typing import Dict

from bs4 import BeautifulSoup
import requests

import utils.db as db
import websoc.settings as websoc
from models.departments_model import DepartmentsModel


def update_departments():
    _save_to_db(_scrape())


def _save_to_db(departments: [Dict]):
    db.clear_all(DepartmentsModel)
    models = [DepartmentsModel(**dept) for dept in departments]
    db.save_list(models)


def _scrape() -> [Dict]:
    source = requests.get(websoc.URL, headers={"User-Agent": websoc.USER_AGENT}).content
    soup = BeautifulSoup(source, "lxml")
    depts = []

    dept_select = soup.find("select", {"name": "Dept"})
    for option in dept_select.find_all("option"):
        if option["value"] == " ALL":
            continue
        depts.append({"code": option["value"], "name": _clean_dept_name(option.text)})

    return depts


def _clean_dept_name(text: str) -> str:
    return text.split(".")[-1]
