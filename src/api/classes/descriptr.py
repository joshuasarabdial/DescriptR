"""Main logic of the Descriptr Python API. Performs searches."""

import json
import os
import sys
import re
import glob
import time

from classes.course_enums import SemesterOffered
from classes.course_parser import CourseParser
from classes.course_encoder import CourseEncoder
from classes.descriptr_searches import DescSearches
from classes.pdf_converter import PDFConverter
from functions.parse_scrape import add_course_capacity
from functions.save_webadvisor_courses import scrape_and_parse_webadvisor_courses


class Descriptr():
    """
    Stores and enables searches of courses within the WebAdvisor course calendar.

    Methods:
        apply_filters(filters):
            Searches using multiple filters in the provided filters dictionary, returning a JSON result
        export_json():
            Generates a JSON representation of carryover_data, with error message if applicable
        list_prereqs():
            Generate array of n1 prerequisites for all courses in the search output.

        do_search_code(args):
            Search by course code.
        do_search_department(args):
            Search by department.
        do_search_keyword(args):
            Search by keyword.
        do_search_level(args):
            Search by course level.
        do_search_number(args):
            Search by exact course number.
        do_search_semester(args):
            Search by semester.
        do_search_weight(args):
            Search by credit weight.
        do_search_lec_hours(args):
            Search by number of lecture hours.
        do_search_lab_hours(args):
            Search by number of lab hours.
        do_search_capacity(args):
            Search by available capacity.
    """

    def __init__(self):
        """Use PDFConverter to convert Course Cal to text. Init cmd loop."""
        filepath = 'c12.pdf'
        if len(sys.argv) > 1:
            for i in range(1, len(sys.argv)):
                if(re.match(".+\\.pdf", sys.argv[i])):
                    filepath = sys.argv[i]
                    break

        self._load(filepath)

        latest_file = None

        if os.getenv("SCRAPE") != "OFF":
            for i in range(0, 2):  # i should only be 0 or 1 (single retry)
                try:
                    latest_file = max(glob.iglob(
                        "webadvisor-courses/*.html"), key=os.path.getctime)
                    if (time.time() - os.path.getctime(latest_file)) > 86400:
                        raise Exception
                    elif i == 0:
                        print(
                            "Retrieved cached WebAdvisor scrape made less than 24h ago. (" + latest_file + ")")
                    else:
                        print(
                            "Successfully scraped and saved WebAdvisor. (" + latest_file + ")")
                    break
                except (ValueError, Exception):
                    if i == 0:  # Only scrape WebAdvisor once to avoid DoS
                        scrape_and_parse_webadvisor_courses()
                    else:
                        print(
                            "[W] Error while scraping WebAdvisor. Courses may not have updated capacity information.")

        self.all_courses = add_course_capacity(self.all_courses)

    def _load(self, filepath):
        """Initialize from PDF."""
        converter = PDFConverter()
        parser = CourseParser()

        converter.openPDF(filepath)

        self.all_courses = parser.open_file("converted-pdf.txt")

        self.carryover_data = []  # A copy of data returned from search here.
        self.n1_prereqs = []
        self.search = DescSearches()

    def apply_filters(self, filters):
        """
        Given an object of filters, performs all searches and returns the results as a JSON.

        @param {String|Dict}    filters     A stringified JSON object or a dictionary of the filters to be applied
        @returns {String} A stringified JSON object of the courses after applying the filters, and an error if applicable
        """
        self.carryover_data = self.all_courses

        try:
            if type(filters) != dict:
                filters = json.loads(filters)

            for key, value in filters.items():
                if key == "code":
                    self.do_search_code(value, carryover=True)
                elif key == "subject":
                    self.do_search_subject(value, carryover=True)
                elif key == "department":
                    self.do_search_department(value, carryover=True)
                elif key == "keyword":
                    self.do_search_keyword(value, carryover=True)
                elif key == "level":
                    self.do_search_level(value, carryover=True)
                elif key == "number":
                    self.do_search_number(value, carryover=True)
                elif key == "semester":
                    self.do_search_semester(value, carryover=True)
                elif key == "weight":
                    self.do_search_weight(value, carryover=True)
                elif key == "capacity":
                    search_capacity = value.get("capacity")
                    search_comparison = value.get("comparison", "=")
                    self.do_search_capacity(
                        f"{search_capacity}", f"{search_comparison}", carryover=True)
                elif key == "lecture":
                    search_hours = value.get("hours")
                    search_comparison = value.get("comparison", "=")
                    self.do_search_lec_hours(
                        f"{search_hours}", f"{search_comparison}", carryover=True)
                elif key == "lab":
                    search_hours = value.get("hours")
                    search_comparison = value.get("comparison", "=")
                    self.do_search_lab_hours(
                        f"{search_hours}", f"{search_comparison}", carryover=True)
                elif key == "offered":
                    self.do_search_offered(value, carryover=True)

            self.prereq_list()

        except Exception as e:
            self.carryover_data = []
            return json.dumps({
                "error": str(e),
                "courses": [],
                "prereqs": [],
            })

        return self.export_json()

    def export_json(self):
        """
        Export a JSON representation of courses contained in the carryover_data.

        @returns {String} JSON object containing an array of courses, and error if applicable
        """
        try:
            return json.dumps({
                "error": None,
                "courses": self.carryover_data,
                "prereqs": self.n1_prereqs,
            }, cls=CourseEncoder)
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "courses": [],
                "prereqs": []
            })

    def prereq_list(self):
        """Generate array of n1 prerequisites for all courses in the search output."""
        simple_prereqs = []

        # Make a list of all simple prereqs of the search results
        for course in self.carryover_data:
            if hasattr(course, "prerequisites"):
                try:
                    for simple_pre in course.prerequisites["simple"]:
                        simple_prereqs.append(simple_pre)
                except KeyError:
                    pass

        # # Remove duplicates from simple_prereqs
        simple_prereqs = list(set(simple_prereqs))

        # Find prereqs and add them to the global n1_prereqs array to be returned in the json res.
        # for pre in simple_prereqs:
        #     for course in self.all_courses:
        #         if pre == course.fullname():
        #             print(f"Appending 1 {course.fullname()}")
        #             self.n1_prereqs.append(course)
        #             break
        #         elif pre == f"{course.code}*{course.number}":
        #             print(f"Appending 2 {course.fullname()}")
        #             self.n1_prereqs.append(course)
        #             break
        self.n1_prereqs = [course for course in self.all_courses if course.fullname() in
                           simple_prereqs]

    def _perform_search(self, args, function, carryover=False, converter=None, join=True):
        search_array = self.carryover_data
        if not carryover:
            search_array = self.all_courses

        search_parameter = None

        if converter is not None:
            search_parameter = converter(args['query'])
        else:
            search_parameter = args['query']

        self.carryover_data = function(search_array, search_parameter, args['comparison'])

    def do_search_code(self, args, carryover=False):
        """
        Search by course code.

        @param {String}     args        The course letters e.g. CIS
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(args, self.search.byCourseCode, carryover=carryover)

    def do_search_subject(self, args, carryover=False):
        """
        Search by course subject.
        @param {String}     args        The course subject e.g. Accounting
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(args, self.search.byCourseSubject, carryover=carryover)

    def do_search_department(self, args, carryover=False):
        """
        Search by course department.

        @param {String}     args        The course department e.g. Department of Clinical Studies
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(args, self.search.byDepartment, carryover=carryover)

    def do_search_keyword(self, args, carryover=False):
        """
        Search by keyword in the course.

        @param {String}     args        The term to search for eg. biology
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(args, self.search.byKeyword, carryover=carryover)

    def do_search_level(self, args, carryover=False):
        """
        Search by level of a course.

        @param {String}     args        The leading number of a course code eg. 4 for a 4XXX course
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(args, self.search.byCourseLevel, carryover=carryover)

    def do_search_number(self, args, carryover=False):
        """
        Search by full course number.

        @param {String}     args        The number of a course eg. 2750
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(args, self.search.byCourseNumber, carryover=carryover)

    def semester_converter(self, semester):
        """Convert string semester into enum."""
        try:
            return SemesterOffered[semester]
        except Exception:
            print("[E] Please enter a supported semester. [F, S, U, W]")
        return

    def do_search_semester(self, args, carryover=False):
        """
        Search by semester.

        @param {String}     args        One of the following codes, [S, F, W, U]
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(args, self.search.bySemester, converter=self.semester_converter, carryover=carryover)

    def weight_converter(self, weight):
        """Convert string weight into float."""
        try:
            return float(weight)
        except Exception:
            print("[E] Not a floating point number or out-of-range.")
        return

    def do_search_weight(self, args, carryover=False):
        """
        Search by credit weight.

        @param {String}     args        The weight of the course. One of [0.0, 0.25, 0.5, 0.75, 1.0, 1.75, 2.0, 2.5, 2.75, 7.5]
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(args, self.search.byWeight, converter=self.weight_converter, carryover=carryover)

    def do_search_capacity(self, *args, carryover=False):
        """
        Search by available capacity.

        @param {String}     args        The available capacity of a course. Must be non-negative.
                                        How to perform the comparision. One of ["=", ">", "<"]. Defaults to "=".
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        search_array = []
        if carryover:
            search_array = self.carryover_data
        else:
            search_array = self.all_courses

        comp = '='
        capacity = ''
        int_capacity = 0.0

        # Find the first code
        for arg in args:
            if arg[0] not in ['-', '=', '>', '<', '>=', '<=']:
                capacity = arg
            elif arg[0] in ['=', '>', '<', '>=', '<=']:
                comp = arg

        try:
            int_capacity = int(capacity)
        except ValueError:
            print("\t[E] Not an integer or out of range.")
            return

        try:
            self.carryover_data = self.search.byCapacity(search_array, int_capacity, comp)
        except ValueError as e:
            print(f"[E]: {e}")

    def do_search_lec_hours(self, *args, carryover=False):
        """
        Search by lecture hours.

        @param {String}     args        The number of hours of lecture for the course. Must be non-negative
                                        How to perform the comparision. One of ["=", ">", "<"]. Defaults to "=".
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        search_array = []
        if carryover:
            search_array = self.carryover_data
        else:
            search_array = self.all_courses

        comp = '='
        hours = ''
        float_hours = 0.0

        # Find the first code
        for arg in args:
            if arg[0] not in ['-', '=', '>', '<', '>=', '<=']:
                hours = arg
            elif arg[0] in ['=', '>', '<', '>=', '<=']:
                comp = arg

        try:
            float_hours = float(hours)
        except ValueError:
            print("\t[E] Not a floating point number. Or out of range")
            return

        try:
            self.carryover_data = self.search.byLectureHours(search_array, float_hours, comp)
        except ValueError as e:
            print(f"[E]: {e}")

    def do_search_lab_hours(self, *args, carryover=False):
        """
        Search by lab hours.

        @param {String}     args        The number of hours of lab for the course. Must be non-negative
                                        How to perform the comparision. One of ["=", ">", "<"]. Defaults to "=".
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        search_array = []
        if carryover:
            search_array = self.carryover_data
        else:
            search_array = self.all_courses

        comp = '='
        hours = ''
        float_hours = 0.0

        # Find the first code
        for arg in args:
            if arg[0] not in ['-', '=', '>', '<', '>=', '<=']:
                hours = arg
            elif arg[0] in ['=', '>', '<', '>=', '<=']:
                comp = arg

        try:
            float_hours = float(hours)
        except ValueError:
            print("\t[E] Not a floating point number. Or out of range")
            return

        try:
            self.carryover_data = self.search.byLabHours(search_array, float_hours, comp)
        except ValueError as e:
            print(f"[E]: {e}")

    def offered_converter(self, offered):
        """Convert offered to boolean."""
        args = offered.split(" ")
        for arg in args:
            if arg.lower() == "y":
                return True
            if arg.lower() == "n":
                return False
        return

    def do_search_offered(self, args, carryover=False):
        """
        Search by if a course is currently offered or not.

        @param {String}     args        Y/N. Only returns offered courses if Y and only returns unoffered courses if N.
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(args, self.search.byOffered, converter=self.offered_converter, carryover=carryover)

    def do_search_course_prerequisites(self, args):
        """
        Retrieve all prerequisites for a specific course.

        @param {String}     args       The course id (<code>*<number>, eg. CIS*2750)
        """
        self._perform_search(args, self.search.getPrerequisiteTree, carryover=False)
