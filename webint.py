from requests import get, Response
from bs4 import BeautifulSoup
import json


def get_soup(url: str) -> BeautifulSoup:
    response: Response = get(url)
    return BeautifulSoup(response.content, "lxml")


def get_course_list(soup: BeautifulSoup) -> list[str]:
    names = soup.find_all(class_="course-name")
    descriptions = soup.find_all(class_="course-descriptions")
    course_info = [
        (name.text + "\n" + description.text).strip()
        for name, description in list(zip(names, descriptions))
    ]
    return course_info


def get_catalog(url: str, domain: str = "catalog") -> list[str]:
    visited: set[str] = set()
    soup: BeautifulSoup = get_soup(url)

    visited.update(
        [
            f'https://catalog.ucsd.edu{link["href"][2:]}'
            for link in soup.find_all("a", href=True)
            if "../courses" in link["href"]
        ]
    )

    return list(visited)


def get_all_courses() -> dict[str, list[str]]:
    catalog = get_catalog("https://catalog.ucsd.edu/front/courses.html")
    courses: dict[str, list[str]] = dict()
    for subject in catalog:
        soup = get_soup(subject)
        courses[subject.split("/")[-1][:-5]] = get_course_list(soup)
    return courses


with open("courses.json", "w") as f:
    json.dump({"courses": get_all_courses()}, f)
