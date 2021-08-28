from classes.course_enums import *
from classes.course_errors import *

# Class for with helpers for validating a course's fields upon creation.


class CourseVal:

    # Method for validating a course's subject.
    def subject(subject):
        if type(subject) != str:
            raise CourseErr.SUBJECT_TYP
        if len(subject) == 0:
            raise CourseErr.SUBJECT_LEN

    # Method for validating a course's departments.
    def departments(departments):
        if type(departments) != list:
            raise CourseErr.DEPARTMENTS_TYPE
        if len(departments) == 0:
            raise CourseErr.DEPARTMENTS_LEN

        for department in departments:
            if isinstance(department, str) == False or len(department) == 0:
                raise CourseErr.DEPARTMENT_TYP

    # Method for validating a course's code.
    def code(code):
        if type(code) != str:
            raise CourseErr.CODE_TYP
        if len(code) == 0:
            raise CourseErr.CODE_LEN

    # Method for validating a course's number.
    def number(number):
        if type(number) != str:
            raise CourseErr.NUMBER_TYP
        if len(number) == 0 or len(number) > 4:
            raise CourseErr.NUMBER_RANGE

    # Method for validating a course's name.
    def name(name):
        if type(name) != str:
            raise CourseErr.NAME_TYP
        if len(name) == 0:
            raise CourseErr.NAME_LEN

    # Method for validating a course's semesters offered.
    def semesters_offered(semesters_offered):
        if type(semesters_offered) != list:
            raise CourseErr.SEMESTERS_OFFERED_TYP

        if len(semesters_offered) == 0:
            raise CourseErr.SEMESTERS_OFFERED_LEN

        for semester_offered in semesters_offered:
            if isinstance(semester_offered, SemesterOffered) == False:
                raise CourseErr.SEMESTER_OFFERED_TYP

    # Method for validating a coure's lecture hours.
    def lecture_hours(lecture_hours):
        if type(lecture_hours) != float:
            raise CourseErr.LEC_HOURS_TYP
        if lecture_hours < 0 or lecture_hours > (24*7):
            raise CourseErr.LEC_HOURS_RANGE

    # Method for validating a course's lab hours.
    def lab_hours(lab_hours):
        if type(lab_hours) != float:
            raise CourseErr.LAB_HOURS_TYP
        if lab_hours < 0 or lab_hours > (24*7):
            raise CourseErr.LAB_HOURS_RANGE

    # Method for evaluating a coure's credits.
    def credits(credits):
        if type(credits) != float:
            raise CourseErr.CREDITS_TYP
        if credits < 0:
            raise CourseErr.CREDITS_RANGE

    # Method for evaluating a course's description.
    def description(description):
        if type(description) != str:
            raise CourseErr.DESCRIPTION_TYP

    # Method for evaluating a course's distance_education.
    def distance_education(distance_education):
        if isinstance(distance_education, DistanceEducation) == False:
            raise CourseErr.DIST_EDUCATION_TYP

    # Method for evaluating a course's year_parity_restrictions.
    def year_parity_restrictions(year_parity_restrictions):
        if isinstance(year_parity_restrictions, YearParityRestrictions) == False:
            raise CourseErr.YEAR_PARITY_RESTR_TYP

    # Method for evaluating a course's other offerings(Offerings that didn't fall under another attribute).
    def other(other):
        if type(other) != str:
            raise CourseErr.OTHER_TYP
        if len(other) == 0:
            raise CourseErr.OTHER_LEN

    # Method for evaulating a course's prerequisites.
    def prerequisites(prerequisites):
        if type(prerequisites) != dict or ("simple" not in prerequisites and "complex" not in prerequisites) or ("original" not in prerequisites):
            raise CourseErr.PREREQ_MISSING_ATTR
        if type(prerequisites["original"]) != str or len(prerequisites["original"]) == 0:
            raise CourseErr.PREREQ_ATTR_ORIGINAL_TYP_OR_LEN
        if "simple" in prerequisites:
            if type(prerequisites["simple"]) != list or len(prerequisites["simple"]) == 0:
                raise CourseErr.PREREQ_ATTR_SIMPLE_TYP_OR_LEN
        if "complex" in prerequisites:
            if type(prerequisites["complex"]) != list or len(prerequisites["complex"]) == 0:
                raise CourseErr.PREREQ_ATTR_COMPLEX_TYP_OR_LEN

    # Method for evaluating a coure's equate(s)
    def equates(equates):
        if type(equates) != str:
            raise CourseErr.EQUATES_TYP
        if len(equates) == 0:
            raise CourseErr.EQUATES_LEN

    # Method for evaluating a course's corequisite(s)
    def corequisites(corequisites):
        if type(corequisites) != str:
            raise CourseErr.COREQ_TYP
        if len(corequisites) == 0:
            raise CourseErr.COREQ_LEN

    # Method for evaluating a course's restriction(s)
    def restrictions(restrictions):
        if type(restrictions) != list:
            raise CourseErr.RESTRICTIONS_TYP
        if len(restrictions) == 0:
            raise CourseErr.RESTRICTIONS_LEN

        for restriction in restrictions:
            if isinstance(restriction, str) == False or len(restriction) == 0:
                raise CourseErr.RESTRICTION_TYP_OR_LEN

    def capacity(cap):
        """
        Validate the passed values for the capacity_max properties.

        Args:
            cap (int): The capacity available for a course.

        Raises:
            CAP_TYP (Exception): If cap is not an int, or if cap is negative.
        """
        if type(cap) != int or cap < 0:
            raise CourseErr.CAP_TYP
