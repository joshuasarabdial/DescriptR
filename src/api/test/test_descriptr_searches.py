import unittest
import os

from classes.descriptr_searches import DescSearches
from classes.course import Course
from classes.course_enums import *

""" Change working directory to one level above here """
os.chdir(os.path.dirname(os.path.dirname(__file__)))


class TestDescSearches(unittest.TestCase):

    single_course = []

    @classmethod
    def setUpClass(self):
        self.single_course = [Course({
            "subject": "Hospitality and Tourism Management",
            "departments": ["School of Hospitality", "Food and Tourism Management"],
            "code": "HTM",
            "number": "4080",
            "name": "Experiential Learning and Leadership in the Service Industry",
            "semesters_offered": [SemesterOffered.F, SemesterOffered.W],
            "lecture_hours": 3.5,
            "lab_hours": 0.0,
            "credits": 0.5,
            "description": "An integration of the students' academic studies with their work experiences. Emphasis\n\
            will be placed on applying and evaluating theoretical concepts in different working environments. \
            Students will investigate the concept of workplace fit applying this to their prospective career path.",
            "distance_education": DistanceEducation.ONLY,
            "year_parity_restrictions": YearParityRestrictions.EVEN_YEARS,
            "other": "Last offering - Winter 2021",
            "prerequisites": {
                "complex":
                    [
                        "14.00 credits and a minimum of 700 hours of verified work experience in the hospitality, sport and tourism industries."
                    ],
                "original": "14.00 credits and a minimum of 700 hours of verified work experience in the hospitality, sport and tourism industries."
            },
            "equates": "HISP*2040",
            "corequisites": "HTM*4075",
            "restrictions": ["MGMT*1000", "Not available to students in the BCOMM program."],
            "capacity_available": 0,
            "capacity_max": 5,
        })]
        self.two_courses = self.single_course + [
            Course({
                "subject": "Computing and Information Science",
                "departments": ["School of Computer Science"],
                "code": "CIS",
                "number": "2250",
                "name": "Software Design II",
                "semesters_offered": [SemesterOffered.W],
                "lecture_hours": float(3),
                "lab_hours": float(2),
                "credits": 0.5,
                "description": "This course focuses on the process of software design. Best practices for code development\n\
                and review will be the examined. The software development process and tools to support \
                this will be studied along with methods for project management. The course has an applied \
                focus and will involve software design and development experiences in teams, a literacy \
                component, and the use of software development tools.",
                "distance_education": DistanceEducation.NO,
                "year_parity_restrictions": YearParityRestrictions.NONE,
                "prerequisites": {
                    "simple":
                        [
                            "CIS*1250",
                            "CIS*1300"
                        ],
                    "original": "CIS*1250, CIS*1300"
                },
                "restrictions": ["Restricted to BCOMP:SENG majors"],
                "capacity_available": 10,
                "capacity_max": 20,
            })
        ]
        self.three_courses = self.two_courses + [
            Course({
                "subject": "Computing and Information Science",
                "departments": ["School of Computer Science"],
                "code": "CIS",
                "number": "3250",
                "name": "Software Design III",
                "semesters_offered": [SemesterOffered.W, SemesterOffered.S],
                "lecture_hours": float(3),
                "lab_hours": float(2),
                "credits": 7.5,
                "description": "Some description here...",
                "distance_education": DistanceEducation.NO,
                "year_parity_restrictions": YearParityRestrictions.NONE,
                "prerequisites": {
                    "simple": [
                        "CIS*2250",
                        "CIS*1300"
                    ],
                    "original": "CIS*2250, CIS*1300"
                },
                "restrictions": ["Restricted to BCOMP:SENG majors"]
            })
        ]

    def test_byCourseCode(self):
        """
            Test that course code search returns correct results
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseCode(self.single_course, "HTM", '=')) == 1)

    def test_byCourseCode_case(self):
        """
            Test that course code search returns correct results regardless of upper/lower case
        """
        upperCode = "HTM"
        lowerCode = "htm"
        mixedCode = "hTm"

        d = DescSearches()
        upperResult = d.byCourseCode(self.single_course, upperCode, '=')
        lowerResult = d.byCourseCode(self.single_course, lowerCode, '=')
        mixedResult = d.byCourseCode(self.single_course, mixedCode, '=')

        self.assertTrue(len(upperResult) == 1)
        self.assertTrue(len(lowerResult) == 1)
        self.assertTrue(len(mixedResult) == 1)

    def test_byCourseCode_contains(self):
        """
            Test that course code search returns correct results for contains comparison
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseCode(self.three_courses, "ci", "~")) == 2)
        self.assertTrue(len(d.byCourseCode(self.three_courses, "h", "~")) == 1)
        self.assertTrue(len(d.byCourseCode(self.three_courses, "CIS", "~")) == 2)
        self.assertTrue(len(d.byCourseCode(self.three_courses, "HTM", "~")) == 1)

    def test_byCourseCode_none(self):
        """
            Test that course code search returns no results for code not in courses
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseCode(self.single_course, "DNE", '=')) == 0)

    def test_byCourseLevel(self):
        """
            Test that course level search returns correct results
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseLevel(self.single_course, "4", '=')) == 1)

    def test_byCourseLevel_invalid(self):
        """
            Test that course level search raises exceptions for invalid numbers
        """
        d = DescSearches()

        with self.assertRaises(Exception) : d.byCourseLevel(self.single_course, "0", '=')
        with self.assertRaises(Exception) : d.byCourseLevel(self.single_course, "11", '=')
        with self.assertRaises(Exception) : d.byCourseLevel(self.single_course, "a", '=')
        with self.assertRaises(Exception) : d.byCourseLevel(self.single_course, 4, '=')

    def test_byCourseLevel_none(self):
        """
            Test that course level search returns no results if no matches are found
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseLevel(self.single_course, "1", '=')) == 0)

    def test_byCourseLevel_greaterThan(self):
        """
            Test that course level search returns correct results for greater than comparison
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "1", ">")) == 3)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "2", ">")) == 2)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "3", ">")) == 1)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "4", ">")) == 0)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "5", ">")) == 0)

    def test_byCourseLevel_greaterThanOrEqualTo(self):
        """
            Test that course level search returns correct results for greater than or equal to comparison
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "1", ">=")) == 3)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "2", ">=")) == 3)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "3", ">=")) == 2)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "4", ">=")) == 1)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "5", ">=")) == 0)

    def test_byCourseLevel_lessThan(self):
        """
            Test that course level search returns correct results for less than comparison
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "1", "<")) == 0)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "2", "<")) == 0)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "3", "<")) == 1)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "4", "<")) == 2)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "5", "<")) == 3)

    def test_byCourseLevel_lessThanOrEqualTo(self):
        """
            Test that course level search returns correct results for less than or equal to comparison
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "1", "<=")) == 0)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "2", "<=")) == 1)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "3", "<=")) == 2)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "4", "<=")) == 3)
        self.assertTrue(len(d.byCourseLevel(self.three_courses, "5", "<=")) == 3)

    def test_byCourseNumber(self):
        """
            Test that course number search returns correct results
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseNumber(self.single_course, "4080", '=')) == 1)

    def test_byCourseNumber_invalid(self):
        """
            Test that course number search raises exceptions for invalid numbers
        """
        d = DescSearches()

        with self.assertRaises(Exception) : d.byCourseNumber(self.single_course, "abcd", '=')
        with self.assertRaises(Exception) : d.byCourseNumber(self.single_course, 1234, '=')
        with self.assertRaises(Exception) : d.byCourseNumber(self.single_course, "11", '=')
        with self.assertRaises(Exception) : d.byCourseNumber(self.single_course, "40801", '=')
        with self.assertRaises(Exception) : d.byCourseNumber(self.single_course, 4, '=')

    def test_byCourseNumber_none(self):
        """
            Test that course number search returns no results if no matches are found
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseNumber(self.single_course, "1234", '=')) == 0)

    def test_byCourseNumber_greaterThan(self):
        """
            Test that course number search returns correct results for greater than comparison
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "1000", ">")) == 3)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "2000", ">")) == 3)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "2250", ">")) == 2)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "3250", ">")) == 1)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "4080", ">")) == 0)

    def test_byCourseNumber_greaterThanOrEqualTo(self):
        """
            Test that course number search returns correct results for greater than or equal to comparison
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "1000", ">=")) == 3)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "2000", ">=")) == 3)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "2250", ">=")) == 3)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "3250", ">=")) == 2)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "4080", ">=")) == 1)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "5000", ">=")) == 0)

    def test_byCourseNumber_lessThan(self):
        """
            Test that course number search returns correct results for less than comparison
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "2000", "<")) == 0)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "2250", "<")) == 0)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "3250", "<")) == 1)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "4080", "<")) == 2)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "5000", "<")) == 3)

    def test_byCourseNumber_lessThanOrEqualTo(self):
        """
            Test that course number search returns correct results for less than or equal to comparison
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "2000", "<=")) == 0)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "2250", "<=")) == 1)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "3250", "<=")) == 2)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "4080", "<=")) == 3)
        self.assertTrue(len(d.byCourseNumber(self.three_courses, "5000", "<=")) == 3)

    def test_byKeyword(self):
        """
            Test that keyword search returns correct results
        """
        d = DescSearches()
        self.assertTrue(len(d.byKeyword(self.single_course, "htm*4080", '=')) == 1)
        self.assertTrue(len(d.byKeyword(self.single_course, "SERVICE", '=')) == 1)
        self.assertTrue(len(d.byKeyword(self.single_course, "hospitality and tourism", '=')) == 1)

    def test_byKeyword_case(self):
        """
            Test that keyword search returns correct results regardless of upper/lower case
        """
        upperWord = "TOURISM"
        lowerWord = "tourism"
        mixedWord = "tOUrIsM"

        d = DescSearches()
        upperResult = d.byKeyword(self.single_course, upperWord, '=')
        lowerResult = d.byKeyword(self.single_course, lowerWord, '=')
        mixedResult = d.byKeyword(self.single_course, mixedWord, '=')

        self.assertTrue(len(upperResult) == 1)
        self.assertTrue(len(lowerResult) == 1)
        self.assertTrue(len(mixedResult) == 1)

    def test_byKeyword_none(self):
        """
            Test that keyword search returns no results for keyword not in courses
        """
        d = DescSearches()
        self.assertTrue(len(d.byKeyword(self.single_course, "does not exist", '=')) == 0)

    def test_byKeyword_invalid(self):
        """
            Test that keyword search raises exceptions for invalid keyword
        """
        d = DescSearches()

        with self.assertRaises(Exception) : d.byKeyword(self.single_course, 5, '=')
        with self.assertRaises(Exception) : d.byKeyword(self.single_course, "", '=')
        with self.assertRaises(Exception) : d.byKeyword(self.single_course, " ", '=')
        with self.assertRaises(Exception) : d.byKeyword(self.single_course, "\n\t", '=')

    def test_byKeyword_whitespace(self):
        """
            Test that keyword search ignores leading and trailing whitespace
        """
        d = DescSearches()
        self.assertTrue(len(d.byKeyword(self.single_course, " htm*4080 ", '=')) == 1)
        self.assertTrue(len(d.byKeyword(self.single_course, "\nhtm*4080\n", '=')) == 1)
        self.assertTrue(len(d.byKeyword(self.single_course, "\thtm*4080\t", '=')) == 1)

    def test_bySemester(self):
        """Test that semester search returns correct results."""
        d = DescSearches()
        self.assertTrue(len(d.bySemester(self.single_course, SemesterOffered.W, '=')) == 1)
        self.assertTrue(len(d.bySemester(self.two_courses, SemesterOffered.F, '=')) == 1)

    def test_bySemester_invalid(self):
        """Test that semester search fails nonconforming input."""
        d = DescSearches()
        with self.assertRaises(Exception):
            d.bySemester(self.single_course, "W", '=')
        with self.assertRaises(Exception):
            d.bySemester(self.single_course, 4, '=')

    def test_byWeight(self):
        """Test that weight search returns correct results."""
        d = DescSearches()
        self.assertTrue(len(d.byWeight(self.two_courses, 0.5, '=')) == 2)
        self.assertTrue(len(d.byWeight(self.single_course, 0.0, '=')) == 0)

    def test_byWeight_invalid(self):
        """Test that weight search fails nonconforming input."""
        d = DescSearches()
        with self.assertRaises(Exception):
            d.byWeight(self.single_course, -1, '=')
        with self.assertRaises(Exception):
            d.byWeight(self.single_course, "sdfdf", '=')

    def test_byWeight_oorange(self):
        """Test that weight search fails out of range input."""
        d = DescSearches()
        with self.assertRaises(Exception):
            d.byWeight(self.single_course, 105.3, '=')
        with self.assertRaises(Exception):
            d.byWeight(self.single_course, 0.22, '=')

    def test_byDepartment(self):
        #Test that department search returns correct results.
        d = DescSearches()
        self.assertTrue(len(d.byDepartment(self.single_course, "Food and Tourism Management", '=')) == 1)
        self.assertTrue(len(d.byDepartment(self.single_course, "School of Hospitality", '=')) == 1)
        self.assertTrue(len(d.byDepartment(self.two_courses, "School of Hospitality", '=')) == 1)
        self.assertTrue(len(d.byDepartment(self.two_courses, "School of Computer Science", '=')) == 1)
        self.assertTrue(len(d.byDepartment(self.three_courses, "School of Computer Science", '=')) == 2)

    def test_byDepartment_non_existant(self):
        #Test that department search returns 0 results when it needs to.
        d = DescSearches()
        self.assertTrue(len(d.byDepartment(self.single_course, "Non-existant. I made this up", '=')) == 0)
        self.assertTrue(len(d.byDepartment(self.two_courses, "", '=')) == 0)
        self.assertTrue(len(d.byDepartment(self.three_courses, "School", '=')) == 0)

    def test_byDepartment_invalid(self):
        #Test that department search fails upon invalid usage.
        d = DescSearches()
        with self.assertRaises(Exception):
            d.byDepartment(self.three_courses, 5, '=')
        with self.assertRaises(Exception):
            d.byDepartment(self.three_courses, True, '=')
        with self.assertRaises(Exception):
            d.byDepartment(self.three_courses, [], '=')
        with self.assertRaises(Exception):
            d.byDepartment(self.three_courses, {}, '=')
        with self.assertRaises(Exception):
            d.byDepartment(self.three_courses, 5.5, '=')

    def test_byDepartment_contains(self):
        """
            Tests that department search returns correct results for contains comparison
        """
        d = DescSearches()
        self.assertTrue(len(d.byDepartment(self.three_courses, "tourism", "~")) == 1)
        self.assertTrue(len(d.byDepartment(self.three_courses, "science", "~")) == 2)
        self.assertTrue(len(d.byDepartment(self.three_courses, "school", "~")) == 3)
        self.assertTrue(len(d.byDepartment(self.three_courses, "hosp", "~")) == 1)

    def test_byLectureHours(self):
        """
            Tests that each comparison (including default) returns correct results
        """
        d = DescSearches()
        self.assertTrue(len(d.byLectureHours(self.three_courses, 3.0)) == 2) # Default is "="
        self.assertTrue(len(d.byLectureHours(self.three_courses, 3.5, "=")) == 1)

        self.assertTrue(len(d.byLectureHours(self.three_courses, 3.6, "<")) == 3)
        self.assertTrue(len(d.byLectureHours(self.three_courses, 3.0, "<=")) == 2)
        
        self.assertTrue(len(d.byLectureHours(self.three_courses, 3.0, ">")) == 1)
        self.assertTrue(len(d.byLectureHours(self.three_courses, 3.0, ">=")) == 3)
        self.assertTrue(len(d.byLectureHours(self.three_courses, 3.5, ">=")) == 1)
        self.assertTrue(len(d.byLectureHours(self.three_courses, 0.0, ">=")) == 3)

    def test_byLectureHours_none(self):
        """
            Tests that each comparison (including default) returns no results for no matches
        """
        d = DescSearches()
        self.assertTrue(len(d.byLectureHours(self.three_courses, 16.0)) == 0) # Default is "="
        self.assertTrue(len(d.byLectureHours(self.three_courses, 1.0, "=")) == 0)

        self.assertTrue(len(d.byLectureHours(self.three_courses, 0.0, "<")) == 0)
        self.assertTrue(len(d.byLectureHours(self.three_courses, 2.9, "<=")) == 0)
        self.assertTrue(len(d.byLectureHours(self.three_courses, 0.0, "<=")) == 0)
        
        self.assertTrue(len(d.byLectureHours(self.three_courses, 3.5, ">")) == 0)
        self.assertTrue(len(d.byLectureHours(self.three_courses, 3.6, ">=")) == 0)

    def test_byLectureHours_invalid(self):
        """
            Tests that search throws exceptions for invalid input
        """
        d = DescSearches()

        with self.assertRaises(Exception):
            d.byLectureHours(self.single_course, -1.0)
        with self.assertRaises(Exception):
            d.byLectureHours(self.single_course, 1)
        with self.assertRaises(Exception):
            d.byLectureHours(self.single_course, 2.0, "A")

    def test_byLabHours(self):
        """
            Tests that each comparison (including default) returns correct results
        """
        d = DescSearches()
        self.assertTrue(len(d.byLabHours(self.three_courses, 2.0)) == 2) # Default is "="
        self.assertTrue(len(d.byLabHours(self.three_courses, 0.0, "=")) == 1)

        self.assertTrue(len(d.byLabHours(self.three_courses, 2.0, "<")) == 1)
        self.assertTrue(len(d.byLabHours(self.three_courses, 3.0, "<")) == 3)
        self.assertTrue(len(d.byLabHours(self.three_courses, 2.0, "<=")) == 3)
        self.assertTrue(len(d.byLabHours(self.three_courses, 0.0, "<=")) == 1)
        
        self.assertTrue(len(d.byLabHours(self.three_courses, 1.0, ">")) == 2)
        self.assertTrue(len(d.byLabHours(self.three_courses, 0.0, ">=")) == 3)
        self.assertTrue(len(d.byLabHours(self.three_courses, 2.0, ">=")) == 2)

    def test_byLabHours_none(self):
        """
            Tests that each comparison (including default) returns no results for no matches
        """
        d = DescSearches()
        self.assertTrue(len(d.byLabHours(self.three_courses, 16.0)) == 0) # Default is "="
        self.assertTrue(len(d.byLabHours(self.three_courses, 1.0, "=")) == 0)
        
        self.assertTrue(len(d.byLabHours(self.three_courses, 0.0, "<")) == 0)
        
        self.assertTrue(len(d.byLabHours(self.three_courses, 3.5, ">")) == 0)
        self.assertTrue(len(d.byLabHours(self.three_courses, 2.1, ">=")) == 0)

    def test_byLabHours_invalid(self):
        """
            Tests that search throws exceptions for invalid input
        """
        d = DescSearches()

        with self.assertRaises(Exception):
            d.byLabHours(self.single_course, -1.0)
        with self.assertRaises(Exception):
            d.byLabHours(self.single_course, 1)
        with self.assertRaises(Exception):
            d.byLabHours(self.single_course, 2.0, "A")

    def test_byOffered(self):
        """
            Tests that offered search returns correct results
        """
        d = DescSearches()
        self.assertTrue(len(d.byOffered(self.three_courses, True, '=')) == 2)
        self.assertTrue(len(d.byOffered(self.three_courses, False, '=')) == 1)

    def test_byOffered_none(self):
        """
            Tests that offered search returns empty array for no matches
        """
        d = DescSearches()
        self.assertTrue(len(d.byOffered([self.three_courses[2]], True, '=')) == 0)
        self.assertTrue(len(d.byOffered(self.single_course, False, '=')) == 0)

    def test_byOffered_invalid(self):
        """
            Tests that offered search throws error for invalid arguments
        """
        d = DescSearches()

        with self.assertRaises(Exception):
            d.byOffered(self.single_course, 1, '=')
        with self.assertRaises(Exception):
            d.byOffered(self.single_course, "true", '=')
        with self.assertRaises(Exception):
            d.byOffered(self.single_course, 1.0, '=')

    def test_byCourseSubject(self):
        '''
            Tests that subject search returns correctly
        '''
        d= DescSearches()
        self.assertTrue(len(d.byCourseSubject(self.single_course, "Hospitality and Tourism Management", '=')) == 1)
        self.assertTrue(len(d.byCourseSubject(self.single_course, "Computing and Information Science", '=')) == 0)
        self.assertTrue(len(d.byCourseSubject(self.two_courses, "Hospitality and Tourism Management", '=')) == 1)
        self.assertTrue(len(d.byCourseSubject(self.two_courses, "Computing and Information Science", '=')) == 1)
        self.assertTrue(len(d.byCourseSubject(self.three_courses, "Hospitality and Tourism Management", '=')) == 1)
        self.assertTrue(len(d.byCourseSubject(self.three_courses, "Computing and Information Science", '=')) == 2)

    def test_byCourseSubject_invalid(self):
        '''
            Tests that subject search fails when fed something invalid
        '''
        d= DescSearches()
        with self.assertRaises(Exception):
            d.byCourseSubject(self.three_courses, 1, '=')
        with self.assertRaises(Exception):
            d.byCourseSubject(self.three_courses, True, '=')
        with self.assertRaises(Exception):
            d.byCourseSubject(self.three_courses, 3.14, '=')
        with self.assertRaises(Exception):
            d.byCourseSubject(self.three_courses, [], '=')

    def test_byCourseSubject_contains(self):
        """
            Test that subject search returns correct results for contains comparison
        """

        d = DescSearches()
        self.assertTrue(len(d.byCourseSubject(self.three_courses, "hosp", "~")) == 1)
        self.assertTrue(len(d.byCourseSubject(self.three_courses, "compu", "~")) == 2)

    def test_byCapacity(self):
        '''
            Test that capacity search returns correctly
        '''
        d = DescSearches()
        self.assertTrue(len(d.byCapacity(self.three_courses, 10)) == 1)
        self.assertTrue(len(d.byCapacity(self.three_courses, 0)) == 1)

        self.assertTrue(len(d.byCapacity(self.three_courses, 0, "<")) == 0)
        self.assertTrue(len(d.byCapacity(self.three_courses, 10, "<")) == 1)
        self.assertTrue(len(d.byCapacity(self.three_courses, 15, "<")) == 2)
        
        self.assertTrue(len(d.byCapacity(self.three_courses, 0, "<=")) == 1)
        self.assertTrue(len(d.byCapacity(self.three_courses, 5, "<=")) == 1)
        self.assertTrue(len(d.byCapacity(self.three_courses, 10, "<=")) == 2)
        self.assertTrue(len(d.byCapacity(self.three_courses, 15, "<=")) == 2)
        
        self.assertTrue(len(d.byCapacity(self.three_courses, 0, ">")) == 1)
        self.assertTrue(len(d.byCapacity(self.three_courses, 5, ">")) == 1)
        self.assertTrue(len(d.byCapacity(self.three_courses, 10, ">")) == 0)

        self.assertTrue(len(d.byCapacity(self.three_courses, 0, ">=")) == 2)
        self.assertTrue(len(d.byCapacity(self.three_courses, 5, ">=")) == 1)
        self.assertTrue(len(d.byCapacity(self.three_courses, 10, ">=")) == 1)
        self.assertTrue(len(d.byCapacity(self.three_courses, 15, ">=")) == 0)

    def test_byCapacity_invalid(self):
        '''
            Test that capacity fails when fed something invalid
        '''
        d = DescSearches()
        with self.assertRaises(Exception):
            d.byCapacity(self.three_courses, "Hello")
        with self.assertRaises(Exception):
            d.byCapacity(self.three_courses, -10)
        with self.assertRaises(Exception):
            d.byCapacity(self.three_courses, 15.2)
        with self.assertRaises(Exception):
            d.byCapacity(self.three_courses, -3.7)
        with self.assertRaises(Exception):
            d.byCapacity(self.three_courses, 10, "x")
        with self.assertRaises(Exception):
            d.byCapacity(self.three_courses, -5, "y")
        with self.assertRaises(Exception):
            d.byCapacity(self.three_courses, -5.12, "z")
    
    def test_getPrerequisiteTree(self):
        '''
            Test that getPrerequisiteTree creates correct tree
        '''
        d = DescSearches()
        results = d.getPrerequisiteTree(self.three_courses, "CIS*3250", None)

        self.assertTrue(type(results['prerequisites'][0]['course']) is Course)
        self.assertTrue(results['prerequisites'][0]['course'].fullname() == "CIS*2250")
        self.assertTrue(len(results['prerequisites'][0]['prerequisites']) == 2)
        self.assertTrue(type(results['prerequisites'][0]['prerequisites'][0]['course']) is str)

    def test_getPrerequisiteTree_not_found(self):
        '''
            Test that getPrerequisiteTree raises an exception if root course can't be found
        '''
        d = DescSearches()
        with self.assertRaises(Exception):
            d.getPrerequisiteTree(self.three_courses, "DNE*1234", None)


if __name__ == '__main__':
    unittest.main()
