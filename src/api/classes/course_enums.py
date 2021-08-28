from enum import Enum

class SemesterOffered(Enum):
	U = 0
	S = 1
	F = 2
	W = 3

class DistanceEducation(Enum):
	NO = None
	SUPPLEMENTARY = "Also offered through Distance Education format."
	ONLY = "Offered through Distance Education format only."

class YearParityRestrictions(Enum):
	NONE = None
	EVEN_YEARS = "Offered in even-numbered years."
	ODD_YEARS = "Offered in odd-numbered years."
