# Custom course error messages.
class CourseErr:
    SUBJECT_TYP                     = Exception("Course subject name must be a string.")
    SUBJECT_LEN                     = Exception("Course subject name can't be an empty string.")

    DEPARTMENTS_TYPE                = Exception("Course departments must be a list.")
    DEPARTMENTS_LEN                 = Exception("Course must be part of at least one department.")
    DEPARTMENT_TYP                  = Exception("All course departments must be non-empty strings.")

    CODE_TYP                        = Exception("Course code must be a string.")
    CODE_LEN                        = Exception("Course code can't be an empty string.")

    NUMBER_TYP                      = Exception("Course number must be a string.")
    NUMBER_RANGE                    = Exception("Course number has invalid range.")

    NAME_TYP                        = Exception("Course name must be a string.")
    NAME_LEN                        = Exception("Course name can't be an empty string.")

    SEMESTERS_OFFERED_TYP           = Exception("Course semesters_offered must be a list.")
    SEMESTERS_OFFERED_LEN           = Exception("Course semester offerings must be specified implicitly")
    SEMESTER_OFFERED_TYP            = Exception("All course semesters offered must be a SemesterOffered enum")

    LEC_HOURS_TYP                   = Exception("Course lecture_hours must be a float.")
    LEC_HOURS_RANGE                 = Exception("Course lecture_hours has invalid range.")

    LAB_HOURS_TYP                   = Exception("Course lab_hours must be a float.")
    LAB_HOURS_RANGE                 = Exception("Course lab_hours has invalid range.")

    CREDITS_TYP                     = Exception("Course credit must be a float.")
    CREDITS_RANGE                   = Exception("Course credit not within allowable range.")

    DESCRIPTION_TYP                 = Exception("If the course has a description, it must be a string.")

    DIST_EDUCATION_TYP              = Exception("All courses must store a distance_education property with an enum type of DistanceEducation.")

    YEAR_PARITY_RESTR_TYP           = Exception("All courses must store a year_parity_restrictions property with an enum type of YearParityRestrictions.")

    OTHER_TYP                       = Exception("Course offering under the other category must be a string.")
    OTHER_LEN                       = Exception("If the course has an offering under the other category, it must have a length.")

    PREREQ_MISSING_ATTR             = Exception("Course prerequisites must be a dictionary with \"simple\" and/or \"complex\" which are non-empty arrays and original attribute being a string.")
    PREREQ_ATTR_ORIGINAL_TYP_OR_LEN = Exception("If the course has a prerequisites, prerequisite[\"original\"] must be a non-empty string.")
    PREREQ_ATTR_SIMPLE_TYP_OR_LEN   = Exception("If the course has a prerequisites[\"simple\"] attribute, the simple prerequisites must be a non-empty array.")
    PREREQ_ATTR_COMPLEX_TYP_OR_LEN  = Exception("If the course has a prerequisites[\"complex\"] attribute, the complex prerequisites must be a non-empty array.")

    EQUATES_TYP                     = Exception("Course equates must be a non-empty string.")
    EQUATES_LEN                     = Exception("If the course has a equates property, the equates can't be an empty string.")

    COREQ_TYP                       = Exception("Course corequisites must be a non-empty string.")
    COREQ_LEN                       = Exception("If the course has a corequisites property, the corequisites can't be an empty string.")

    RESTRICTIONS_TYP                = Exception("Course restrictions must be a list of non-empty string.")
    RESTRICTIONS_LEN                = Exception("If the course has a restrictions property, there must be at least one restriction.")
    RESTRICTION_TYP_OR_LEN          = Exception("All course restrictions must be non-empty strings.")

    CAP_TYP = Exception("Available or maximum capacity of a course should be a non-negative integer.")


