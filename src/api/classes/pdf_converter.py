"""
    pdf_converter.py        Andrew D'Agostino

    Uses pdftotext to convert a pdf file to text
"""

import os
import re

class PDFConverter:
    """
        Converts PDF files to text files
    """

    def openPDF(self, filepath):
        """
            Wrapper function to convert and read the PDF file
            @param {String} filepath    The path to the pdf file
            @returns {String}   Returns the converted text, or None if conversion failed
        """
        try:
            self._convertPDF(filepath)
            return self._readConvertedPDF()
        except Exception as e:
            print(e)
            return None

    def _readConvertedPDF(self):
        """
            Reads and returns the converted pdf file as a string
            @returns {String} The contents of the converted text file
            @raises {Exception} If intermediary file cannot be found
        """

        file = open("./converted-pdf.txt", "r")
        if file is None:
            raise Exception("Failed to read converted text file")

        contents = file.read()
        file.close()

        return contents

    def _convertPDF(self, filepath):
        """
            Converts the pdf file at the provided filepath to text
            @param {String} filepath    Path to pdf file
            @raises {Exception} If file has invalid filetype or conversion fails
        """

        if not re.match(".+\\.pdf", filepath, re.IGNORECASE):
            raise Exception("Invalid filetype")

        exit_code = os.system("pdftotext -raw -q -f 7 -eol unix -enc UTF-8 -nopgbrk %s converted-pdf.txt" % filepath)
        if exit_code != 0:
            raise Exception("Failed to convert PDF to text file")
