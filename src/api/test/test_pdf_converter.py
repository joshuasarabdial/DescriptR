import unittest
import os

from classes.pdf_converter import PDFConverter

""" Change working directory to one level above here """
os.chdir(os.path.dirname(os.path.dirname(__file__)))

class TestPDFConverter(unittest.TestCase):

    def test_openPDF(self):
        """
            Test that openPDF() successfully creates and opens a text version
            of the PDF file
        """
        os.system("rm -f converted-pdf.txt")

        c = PDFConverter()
        contents = c.openPDF("c12.pdf")

        f = open("converted-pdf.txt")
        self.assertTrue(f is not None)
        f.close()

        self.assertTrue(contents is not None)

    def test__readConvertedPDF(self):
        """
            Test conversion file successfully read
        """
        c = PDFConverter()
        c._convertPDF("c12.pdf")

        self.assertTrue(c._readConvertedPDF() is not None)

    def test__readConvertedPDF_filenotfound(self):
        """
            Test exception thrown if converted file not found
        """
        os.system("rm -f converted-pdf.txt")

        with self.assertRaises(Exception) : c._readConvertedPDF()

    def test__convertPDF(self):
        """
            Test text file created after success
        """
        os.system("rm -f converted-pdf.txt")

        c = PDFConverter()
        c._convertPDF("c12.pdf")

        f = open("converted-pdf.txt")
        self.assertTrue(f is not None)
        f.close()

    def test__convertPDF_filetype(self):
        """
            Test that exception raised for invalid filetype
        """
        c = PDFConverter()
        with self.assertRaises(Exception) : c._convertPDF("readme.md")

if __name__ == '__main__':
    unittest.main()