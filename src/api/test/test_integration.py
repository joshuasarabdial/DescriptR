import unittest
import os

from classes.descriptr_searches import DescSearches
from classes.course import Course
from classes.course_enums import *
from classes.course_parser import CourseParser
from classes.pdf_converter import PDFConverter

""" Change working directory to one level above here """
os.chdir(os.path.dirname(os.path.dirname(__file__)))

class TestIntegration(unittest.TestCase):

	@classmethod
	def setUpClass(self):

		self.search = DescSearches()

		converter = PDFConverter()
		converter.openPDF("./c12.pdf")

		parser = CourseParser()
		self.courses = parser.open_file("converted-pdf.txt")

	def test_findCIS4250(self):
		socsCourses = self.search.byDepartment(self.courses, "School of Computer Science", "=")
		cisCourses = self.search.byCourseCode(socsCourses, "CIS", "=")
		fourthYearCourses = self.search.byCourseLevel(cisCourses, "4", "=")
		cis4250 = self.search.byCourseNumber(fourthYearCourses,"4250", "=")
		
		self.assertTrue(cis4250[0].code == "CIS" and cis4250[0].number == "4250")

	def test_findENVS1060(self):
		oneCreditCourses = self.search.byWeight(self.courses, 0.5, "=")
		summerCourses = self.search.bySemester(oneCreditCourses, SemesterOffered.S, "=")
		soesCourses = self.search.byDepartment(summerCourses, "School of Environmental Sciences", "=")
		firstYearCourses = self.search.byCourseLevel(soesCourses, "1", "=")
		envsCourses = self.search.byCourseCode(firstYearCourses, "ENVS", "=")
		envs1060 = self.search.byCourseNumber(envsCourses, "1060", "=")

		self.assertTrue(envs1060[0].code == "ENVS" and envs1060[0].number == "1060")

	def test_languageKeyword(self):
		languageKeywordCourses = self.search.byKeyword(self.courses, "language", "=")
		englishKeywordCourses = self.search.byKeyword(languageKeywordCourses, "english", "=")
		frenchKeywordCourses = self.search.byKeyword(englishKeywordCourses, "french", "=")
		fallCourses = self.search.bySemester(frenchKeywordCourses, SemesterOffered.F, "=")

		self.assertTrue(fallCourses[0].code == "FREN" and fallCourses[0].number == "3500")

if __name__ == '__main__':
	unittest.main()