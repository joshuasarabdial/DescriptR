import os
import unittest
from classes.pdf_converter import PDFConverter
from classes.course_parser import *

""" Change working directory to one level above here """
os.chdir(os.path.dirname(os.path.dirname(__file__)))

class TestCourseParser(unittest.TestCase):

    def test_open_file_simple(self):
        '''
            Tests that a Course object can be created from a text file. Also parses the text file.
        '''

        f = open("./test/test-text/typical-course.txt")
        self.assertTrue(f is not None)
        f.close()

        cp = CourseParser()
        courses = cp.open_file("./test/test-text/typical-course.txt")

        self.assertTrue(courses is not None)
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].subject, "Accounting")
        self.assertEqual(courses[0].departments, ["Department of Management"])
        self.assertEqual(courses[0].code, "ACCT")
        self.assertEqual(courses[0].number, "1220")
        self.assertEqual(courses[0].name, "Introductory Financial Accounting")
        self.assertEqual(courses[0].semesters_offered, [SemesterOffered.F, SemesterOffered.W])
        self.assertEqual(courses[0].lecture_hours, 3.0)
        self.assertEqual(courses[0].lab_hours, 0.0)
        self.assertEqual(courses[0].credits, 0.50)
        self.assertEqual(courses[0].description,    "This introductory course is designed to develop a foundational understanding of current"
                                                    + " accounting principles and their implication for published financial reports of business"
                                                    + " enterprises. It builds the base of knowledge and understanding required to succeed in"
                                                    + " more advanced study of accounting. The course approaches the subject from the point"
                                                    + " of view of the user of accounting information rather than that of a person who supplies"
                                                    + " the information.")
        self.assertEqual(courses[0].distance_education, DistanceEducation.SUPPLEMENTARY)
        self.assertEqual(courses[0].restrictions,   ["ACCT*2220 , This is a Priority Access Course. Enrolment may be"
                                                    + " restricted to particular programs or specializations. See department for"
                                                    + " more information."])

    def test_open_file_complex(self):
        '''
            Tests that a more complex course can be parsed and put into a Course structure
        '''

        f = open("./test/test-text/complex-course.txt")
        self.assertTrue(f is not None)
        f.close()

        cp = CourseParser()
        courses = cp.open_file("./test/test-text/complex-course.txt")

        self.assertTrue(courses is not None)
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].subject, "Subject")
        self.assertEqual(courses[0].departments, ["Department of Management", "Department of Science"])
        self.assertEqual(courses[0].code, "ASDF")
        self.assertEqual(courses[0].number, "1234")
        self.assertEqual(courses[0].name, "A complex Example")
        self.assertEqual(courses[0].semesters_offered, [SemesterOffered.U])
        self.assertEqual(courses[0].lecture_hours, 0.0)
        self.assertEqual(courses[0].lab_hours, 0.0)
        self.assertEqual(courses[0].credits, 0.75)
        self.assertEqual(courses[0].description, "Short descript with one line to test for next line peek test")
        self.assertEqual(courses[0].distance_education, DistanceEducation.ONLY)
        self.assertEqual(courses[0].year_parity_restrictions, YearParityRestrictions.EVEN_YEARS)
        self.assertEqual(courses[0].prerequisites, {"simple": ["ACCT*4220"], "original": "ACCT*4220"})
        self.assertEqual(courses[0].corequisites, "MUSC*2180")
        self.assertEqual(courses[0].equates, "CLAS*2150")
        self.assertEqual(courses[0].restrictions,   ["AAAA*1111 , This is a Priority Access Course.",
                                                    "Enrolment may be restricted to particular programs or specializations."
                                                    + " See department for more information."])

    def test_open_file_prereq(self):
        '''
            Tests that the prerequisites field gets parsed into simple, complex and original combinations.
        '''

        f = open("./test/test-text/prereq-filled-course.txt")
        self.assertTrue(f is not None)
        f.close()

        cp = CourseParser()
        courses = cp.open_file("./test/test-text/prereq-filled-course.txt")

        self.assertTrue(courses is not None)
        self.assertEqual(len(courses), 3)
        self.assertEqual(courses[0].subject, "Agriculture")
        self.assertEqual(courses[0].departments, ["Department of Plant Agriculture"])
        self.assertEqual(courses[0].code, "AGR")
        self.assertEqual(courses[0].number, "2150")
        self.assertEqual(courses[0].name, "Plant Agriculture for International Development")
        self.assertEqual(courses[0].semesters_offered, [SemesterOffered.F])
        self.assertEqual(courses[0].lecture_hours, 3.0)
        self.assertEqual(courses[0].lab_hours, 0.0)
        self.assertEqual(courses[0].credits, 0.50)
        self.assertEqual(courses[0].description, "This course will provide students interested in international development with an"
                                                 + " introductory mechanistic understanding of the biology underlying crop production in"
                                                 + " developing nations. Emphasis will be placed on simple, low-cost solutions from biology"
                                                 + " that have the potential to aid efforts in international development. This course is accessible"
                                                 + " to science and non-science students.")
        self.assertEqual(courses[0].distance_education, DistanceEducation.NO)
        self.assertEqual(courses[0].year_parity_restrictions, YearParityRestrictions.NONE)
        self.assertEqual(courses[0].prerequisites, {"complex": ["4.00 credits"],
                                                    "original": "4.00 credits"})
        self.assertEqual(courses[0].restrictions,   ["AGR*2470"])

        self.assertEqual(courses[1].subject, "Agriculture")
        self.assertEqual(courses[1].departments, ["Department of Plant Agriculture", "Department of Animal Biosciences"])
        self.assertEqual(courses[1].code, "AGR")
        self.assertEqual(courses[1].number, "3450")
        self.assertEqual(courses[1].name, "Research Methods in Agricultural Science")
        self.assertEqual(courses[1].semesters_offered, [SemesterOffered.F])
        self.assertEqual(courses[1].lecture_hours, 3.0)
        self.assertEqual(courses[1].lab_hours, 2.0)
        self.assertEqual(courses[1].credits, 0.50)
        self.assertEqual(courses[1].description, "This course provides students with an opportunity to enhance their understanding of the"
                                                 + " principles and processes of agricultural research. The course will provide students with"
                                                 + " a foundation in critical thinking, experimental design and data analysis that will be"
                                                 + " applicable to independent research projects and graduate studies. Students will also"
                                                 + " explore the practical requirements and limitations of scientific research. Laboratory and"
                                                 + " field safety, animal care, intellectual property and research ethics will be reviewed."
                                                 + " Students will be required to practice both oral presentation and writing skills as core"
                                                 + " components of their evaluation.")
        self.assertEqual(courses[1].distance_education, DistanceEducation.NO)
        self.assertEqual(courses[1].year_parity_restrictions, YearParityRestrictions.NONE)
        self.assertEqual(courses[1].prerequisites, {"simple": ["GEOG*2460","STAT*2040","STAT*2060","STAT*2080"],
                                                    "complex": ["Completion of 7.50 credits"], 
                                                    "original": "Completion of 7.50 credits including (1 of GEOG*2460, STAT*2040 , STAT*2060, STAT*2080)"})
        self.assertEqual(courses[1].restrictions,   ["Enrollment in the BSC(AGR), BBRM, BSC.ABIO, BSC.PLSC or"
                                                     + " Minor in Agriculture."])

        self.assertEqual(courses[2].subject, "Art History")
        self.assertEqual(courses[2].departments, ["School of Fine Art and Music"])
        self.assertEqual(courses[2].code, "ARTH")
        self.assertEqual(courses[2].number, "3010")
        self.assertEqual(courses[2].name, "Contemporary Canadian Art")
        self.assertEqual(courses[2].semesters_offered, [SemesterOffered.F])
        self.assertEqual(courses[2].lecture_hours, 3.0)
        self.assertEqual(courses[2].lab_hours, 0.0)
        self.assertEqual(courses[2].credits, 0.50)
        self.assertEqual(courses[2].description, "The wide range of contemporary Canadian visual arts, from painting to new technological"
                                                 + " media, from 'high' culture to punk, will be examined in the context of specifically Canadian"
                                                 + " social and historical conditions during the modern and post-modern periods.")
        self.assertEqual(courses[2].distance_education, DistanceEducation.NO)
        self.assertEqual(courses[2].year_parity_restrictions, YearParityRestrictions.EVEN_YEARS)
        self.assertEqual(courses[2].prerequisites, {"complex": ["7.50 credits or 1.50 credits in Art History."], 
                                                    "original": "7.50 credits or 1.50 credits in Art History."})
