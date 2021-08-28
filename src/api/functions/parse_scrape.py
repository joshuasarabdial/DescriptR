"""
Set of functions that operate on an HTML file scraped with functions/save_webadvisor_courses.py.

Functions:
    parse_html(filename):
        Parses passed HTML file with BeautifulSoup. Returns a dict of extracted results.
"""

from bs4 import BeautifulSoup
import glob
import os
import re


def parse_html():
    """
    Open the last modified HTML file in the scrape directory. Parse with BeautifulSoup. Extract
    course capacity information.

    Returns:
        extracted_info (dict) : A dict of full course codes (TOX*3360) mapped to a subdict of
            information. Ex.
            {
                'TOX*3360': {
                    'code': 'TOX',
                    'number': '3360',
                    'capacity_available: 32 (int),
                    'capacity_max: 90 (int)
                }
                ...
            }
    """
    extracted_info = {}

    glob_res = glob.iglob("webadvisor-courses/*.html")

    try:
        latest_file = max(glob_res, key=os.path.getctime)
    except ValueError as e:
        print(f"[W] Glob unable to find an html file from scraper. Using text file.\n{e}")
        latest_file = "test/test-text/scrape.html"

    with open(latest_file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        rows = soup.find_all("tr")

        for row in rows:
            try:
                cap_str = row.find("td", class_="LIST_VAR5").find("p").contents[0]
                section_str = row.find("a").contents[0]

                # Breakdown capacity string
                capacity_tup = re.match(r"(\d+).*?(\d+)", cap_str).group(1, 2)
                """
                    Regex breakdown:
                    - '(' open capture group
                        - '\d+' One or more decimal characters 0-9
                    - ')' close capture group
                    - '.*?' Zero or more of any character, non-greedy
                    - '(' open capture group
                        - '\d+' One or more decimal characters 0-9
                    - ')' close capture group
                """

                # Breakdown course code*number
                sec_match = re.match(r"^([A-Z]+)\*(\d+)", section_str)
                """
                    Regex breakdown:
                    - '^' beginning of line
                    - '(' open capture group
                        - '[A-Z]+' One or more characters in class A-Z, capital letters.
                    - ')' close capture group
                    - '\*' a literal asterisk character
                    - '(' open capture group
                        - '\d+' One or more decimal characters 0-9
                    - ')' close capture group
                """
                sec_tup = sec_match.group(1, 2)
                sec = sec_match.group(0)

                try:
                    # Search dict for course code
                    # if key exists, add up capacity values and update entry.
                    course = extracted_info[sec]
                    new_vals = {
                            "capacity_available": int(course['capacity_available']) +
                            int(capacity_tup[0]),
                            "capacity_max": int(course['capacity_max']) + int(capacity_tup[1])
                            }
                    extracted_info[sec].update(new_vals)
                except KeyError:
                    # else, create a new entry.
                    extracted_info[sec] = {
                            "code": sec_tup[0],
                            "number": sec_tup[1],
                            "capacity_available": int(capacity_tup[0]),
                            "capacity_max": int(capacity_tup[1])
                            }
            except AttributeError:
                pass
    return extracted_info


def add_course_capacity(courses):
    """
    Combine list of Courses with corresponding capacity info, if available.

    Args:
        courses (list(Course)): The list of courses to merge.

    Returns:
        courses (list(Course)): The list of courses with capacity properties added.
    """
    capacity_info = parse_html()

    for course in courses:
        created_key = f"{course.code}*{course.number}"
        match = capacity_info.get(created_key)
        if match:
            # print(f"TODO\t{created_key}, ")
            # print(f"TODO\t{match['capacity_available']} ({type(match['capacity_available'])})")
            # print(f"TODO\t{match['capacity_max']} ({type(match['capacity_max'])})")
            course.capacity_available = match['capacity_available']
            course.capacity_max = match['capacity_max']

    return courses
