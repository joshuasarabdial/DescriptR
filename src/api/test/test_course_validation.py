import unittest
import os

from classes.course_validation import CourseVal
from classes.course_enums import *


class TestCourseVal(unittest.TestCase):

    def test_subject(self):
        """ Test that valid subject does not raise exception """
        try:
            CourseVal.subject("test")
        except Exception:
            self.fail()

    def test_subject_invalid_type(self):
        """ Test that non-string subject raises exception """
        with self.assertRaises(Exception):
            CourseVal.subject(1234)

    def test_subject_length(self):
        """ Test that zero-length subject raises exception """
        with self.assertRaises(Exception):
            CourseVal.subject("")

    def test_departments(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.departments(["test"])
        except Exception:
            self.fail()

    def test_departments_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.departments(1234)
        with self.assertRaises(Exception):
            CourseVal.departments([1234])
        with self.assertRaises(Exception):
            CourseVal.departments([""])

    def test_departments_length(self):
        """ Test that zero-length raises exception """
        with self.assertRaises(Exception):
            CourseVal.departments([])

    def test_code(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.code("test")
        except Exception:
            self.fail()

    def test_code_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.code(1234)

    def test_code_length(self):
        """ Test that zero-length raises exception """
        with self.assertRaises(Exception):
            CourseVal.code("")

    def test_number(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.number("1234")
        except Exception:
            self.fail()

    def test_number_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.number(1234)

    def test_number_length(self):
        """ Test that zero-length raises exception """
        with self.assertRaises(Exception):
            CourseVal.number("")
        with self.assertRaises(Exception):
            CourseVal.number("12345")

    def test_name(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.name("test")
        except Exception:
            self.fail()

    def test_name_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.name(1234)

    def test_name_length(self):
        """ Test that zero-length raises exception """
        with self.assertRaises(Exception):
            CourseVal.name("")

    def test_semesters_offered(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.semesters_offered([SemesterOffered.W])
        except Exception:
            self.fail()

    def test_semesters_offered_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.semesters_offered(1234)
        with self.assertRaises(Exception):
            CourseVal.semesters_offered([1234])
        with self.assertRaises(Exception):
            CourseVal.semesters_offered([""])

    def test_semesters_offered_length(self):
        """ Test that zero-length raises exception """
        with self.assertRaises(Exception):
            CourseVal.semesters_offered([])

    def test_lecture_hours(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.lecture_hours(3.14)
        except Exception:
            self.fail()

    def test_lecture_hours_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.lecture_hours("3.14")
        with self.assertRaises(Exception):
            CourseVal.lecture_hours(-3.14)
        with self.assertRaises(Exception):
            CourseVal.lecture_hours(float(24*8))

    def test_lab_hours(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.lab_hours(3.14)
        except Exception:
            self.fail()

    def test_lab_hours_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.lab_hours("3.14")
        with self.assertRaises(Exception):
            CourseVal.lab_hours(-3.14)
        with self.assertRaises(Exception):
            CourseVal.lab_hours(float(24*8))

    def test_credits(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.credits(0.5)
        except Exception:
            self.fail()

    def test_credits_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.credits("0.5")
        with self.assertRaises(Exception):
            CourseVal.credits(-0.5)

    def test_description(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.description("test")
        except Exception:
            self.fail()

    def test_description_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.description(1234)

    def test_distance_education(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.distance_education(DistanceEducation.NO)
        except Exception:
            self.fail()

    def test_distance_education_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.distance_education(1234)

    def test_year_parity_restrictions(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.year_parity_restrictions(
                YearParityRestrictions.EVEN_YEARS)
        except Exception:
            self.fail()

    def test_year_parity_restrictions_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.year_parity_restrictions(1234)

    def test_other(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.other("test")
        except Exception:
            self.fail()

    def test_other_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.other(1234)

    def test_other_length(self):
        """ Test that zero-length raises exception """
        with self.assertRaises(Exception):
            CourseVal.other("")

    def test_prerequisites(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.prerequisites({
                "simple": ["test"],
                "complex": ["test"],
                "original": "test"
            })
            CourseVal.prerequisites({
                "simple": ["test"],
                "original": "test"
            })
            CourseVal.prerequisites({
                "complex": ["test"],
                "original": "test"
            })
        except Exception:
            self.fail()

    def test_prerequisites_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.prerequisites("test")
        with self.assertRaises(Exception):
            CourseVal.prerequisites({"original": "test"})
        with self.assertRaises(Exception):
            CourseVal.prerequisites({"simple": ["test"]})
        with self.assertRaises(Exception):
            CourseVal.prerequisites({"original": 1234, "simple": ["test"]})
        with self.assertRaises(Exception):
            CourseVal.prerequisites({"original": "", "simple": ["test"]})
        with self.assertRaises(Exception):
            CourseVal.prerequisites({"original": "test", "simple": 1234})
        with self.assertRaises(Exception):
            CourseVal.prerequisites({"original": "test", "simple": []})
        with self.assertRaises(Exception):
            CourseVal.prerequisites({"original": "test", "complex": 1234})
        with self.assertRaises(Exception):
            CourseVal.prerequisites({"original": "test", "complex": []})

    def test_equates(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.equates("test")
        except Exception:
            self.fail()

    def test_equates_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.equates(1234)

    def test_equates_length(self):
        """ Test that zero-length raises exception """
        with self.assertRaises(Exception):
            CourseVal.equates("")

    def test_corequisites(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.corequisites("test")
        except Exception:
            self.fail()

    def test_corequisites_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.corequisites(1234)

    def test_corequisites_length(self):
        """ Test that zero-length raises exception """
        with self.assertRaises(Exception):
            CourseVal.corequisites("")

    def test_restrictions(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.restrictions(["test"])
        except Exception:
            self.fail()

    def test_restrictions_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.restrictions(1234)
        with self.assertRaises(Exception):
            CourseVal.restrictions([1234])
        with self.assertRaises(Exception):
            CourseVal.restrictions([""])
        with self.assertRaises(Exception):
            CourseVal.restrictions([])

    def test_capacity(self):
        """ Test that valid args does not raise exception """
        try:
            CourseVal.capacity(1234)
        except Exception:
            self.fail()

    def test_capacity_invalid_type(self):
        """ Test that invalid type raises exception """
        with self.assertRaises(Exception):
            CourseVal.capacity("1234")
        with self.assertRaises(Exception):
            CourseVal.capacity(-1234)
