"""
Provides DescSearches, a collection of Course Calendar search functions.

Classes:

    DescSearches
"""

from classes.course_enums import SemesterOffered


class DescSearches:
    """
    A collection of search functions.

    Methods:
        bySemester(courses, semester):
            Search courses by semester.
    """

    def bySemester(self, courses, semester, comparison):
        """
        Filter the passed array of courses by passed semester.

        Args:
            courses (list<Course>): An array of Course data structures.
            semester (Enum SemesterOffered): A supported semester code.

        Raises:
            ValueError (Exception): If semester is not in SemesterOffered Enum.

        Returns:
            (list): A list of courses in the passed semester
        """
        returnCourses = []

        if not isinstance(semester, SemesterOffered):
            raise ValueError("Code not supported. Not in SemesterOffered enum")

        for course in courses:
            if semester in course.semesters_offered:
                returnCourses.append(course)
        return returnCourses

    def byCourseCode(self, courses, code, comparison):
        """
        Filter the passed array of courses by passed course code (eg. ACCT, CIS).

        Args:
            courses (List<Course>): An array of Course data structures.
            code (String): The letter portion of a course's id (eg. CIS, ECON)

        Returns:
            (list): A list of courses with the supplied course code
        """

        returnCourses = []

        for course in courses:
            if comparison == '=':
                if code.lower() == course.code.lower():
                    returnCourses.append(course)
            elif comparison == '~':
                if code.lower() in course.code.lower():
                    returnCourses.append(course)

        return returnCourses

    def byCourseSubject(self, courses, subject, comparison):
        """
        Filter the passed array of courses by passed course subject (eg. Accounting, Computing and Information Science).

        Args:
            courses (List<Course>): An array of Course data structures.
            subject (String): The subject under which a course falls into (eg. Accounting, Computing and Information Science)

        Returns:
            (list): A list of courses with the supplied subject
        """

        returnCourses = []

        if type(subject) != str:
            raise ValueError("Subject must be a string.")

        for course in courses:
            if comparison == '=':
                if subject.lower() == course.subject.lower():
                    returnCourses.append(course)
            elif comparison == '~':
                if subject.lower() in course.subject.lower():
                    returnCourses.append(course)

        return returnCourses

    def byCourseLevel(self, courses, level, comparison):
        """
        Filter the passed array of courses by passed course level

        Args:
            courses (List<Course>): An array of Course data structures.
            level (String): The leading digit of the course number as a string

        Raises:
            ValueError (Exception): If level is not a string digit between 1 and 9

        Returns:
            (list): A list of courses with course numbers starting with the passed digit
        """

        returnCourses = []

        if type(level) != str or not level.isdigit():
            raise ValueError("Course level must be a string digit")

        if len(level) != 1 or level == "0":
            raise ValueError("Course level has invalid range")

        for course in courses:
            if comparison == '=':
                if course.number.startswith(level):
                    returnCourses.append(course)
            elif comparison == '>':
                if int(course.number) > (int(level) + 1) * 1000 - 1:
                    returnCourses.append(course)
            elif comparison == '<':
                if int(course.number) < int(level) * 1000:
                    returnCourses.append(course)
            elif comparison == '>=':
                if int(course.number) >= int(level) * 1000:
                    returnCourses.append(course)
            elif comparison == '<=':
                if int(course.number) <= (int(level) + 1) * 1000 - 1:
                    returnCourses.append(course)

        return returnCourses

    def byCourseNumber(self, courses, number, comparison):
        """
        Filter the passed array of courses by passed course number (eg. 1250, 4720).

        Args:
            courses (List<Course>): An array of Course data structures.
            number (String): The 4-digit number of a course as a string

        Raises:
            ValueError (Exception): If number is not a 4-digit string

        Returns:
            (list): A list of courses with matching course numbers
        """

        returnCourses = []

        if type(number) != str or not number.isdigit():
            raise ValueError("Course number must be a string of digits")

        if len(number) != 4:
            raise ValueError("Course number has invalid range")

        for course in courses:
            if comparison == '=':
                if course.number == number:
                    returnCourses.append(course)
            if comparison == '>':
                if int(course.number) > int(number):
                    returnCourses.append(course)
            if comparison == '<':
                if int(course.number) < int(number):
                    returnCourses.append(course)
            if comparison == '>=':
                if int(course.number) >= int(number):
                    returnCourses.append(course)
            if comparison == '<=':
                if int(course.number) <= int(number):
                    returnCourses.append(course)

        return returnCourses

    def byDepartment(self, courses, department, comparison):
        """
        Filter the passed list of courses by passed department (eg. Department of Clinical Studies).

        Args:
            courses (List<Course>): A list of Course data structures.
            department (String): The department of which a course is a part of (eg. Department of Clinical Studies)

        Returns:
            (list): A list of courses with the supplied department

        """

        if type(department) != str:
            raise ValueError("Department must be a string.")

        returnCourses = []

        for course in courses:
            for dep in course.departments:
                if comparison == '=':
                    if department.lower() == dep.lower().strip():
                        returnCourses.append(course)
                        break
                elif comparison == '~':
                    if department.lower() in dep.lower().strip():
                        returnCourses.append(course)
                        break

        return returnCourses

    def byKeyword(self, courses, keyword, comparison):
        """
        Filter the passed array of courses by passed keyword

        Args:
            courses (List<Course>): An array of Course data structures.
            keyword (String): Word to search through course fields for

        Raises:
            ValueError (Exception): If keyword is not a non-empty string

        Returns:
            (list): A list of courses containing the keyword
        """

        returnCourses = []

        if type(keyword) != str:
            raise ValueError("Keyword must be a string")

        keyword = keyword.strip().lower() # Remove extra whitespace and change to lowercase

        if len(keyword) == 0:
            raise ValueError("Keyword must be non-empty")

        for course in courses:
            if keyword in course.__str__().lower():
                returnCourses.append(course)

        return returnCourses

    def byWeight(self, courses, weight, comparison):
        """
        Filter the passed array of courses by passed weight.

        Args:
            courses(list<Course>): An array of Course data.
            weight: (float): The weight of the credit of the course.

        Raises:
            ValueError (Exception): If weight is not float, or not in range.

        Returns:
            (list): A list of courses with matching course numbers.
        """
        returnCourses = []
        supported = [0.0, 0.25, 0.5, 0.75, 1.0, 1.75, 2.0, 2.5, 2.75, 7.5]

        if type(weight) != float:
            raise ValueError("Weight must be a floating point number")

        if weight not in supported:
            raise ValueError(f"Weight out of range. Must be one of {supported}")

        for course in courses:
            if course.credits == weight:
                returnCourses.append(course)

        return returnCourses

    def byCapacity(self, courses, capacity, comp="="):
        """
        Filter the passed array of courses by available capacity using the provided comparison

        Args:
            courses(list<Course>): An array of Course data.
            capacity: (int): The available capacity in the course
            [comp]: (string): How to compare the capacity (one of =,<,>), defaults to =

        Raises:
            ValueError (Exception): If capacity is negative or comp is invalid

        Returns:
            (list): A list of courses with matching capacity
        """
        returnCourses = []
        comparisons = ["=", "<", ">", ">=", "<="]

        if type(capacity) != int:
            raise ValueError("Capacity must be an integer")

        if capacity < 0:
            raise ValueError("Capacity must not be negative")

        if comp not in comparisons:
            raise ValueError(f"Comparison must be one of {comparisons}")

        for course in courses:
            if hasattr(course, "capacity_available"):
                if comp == "=" and course.capacity_available == capacity:
                    returnCourses.append(course)
                elif comp == ">" and course.capacity_available > capacity:
                    returnCourses.append(course)
                elif comp == "<" and course.capacity_available < capacity:
                    returnCourses.append(course)
                elif comp == "<=" and course.capacity_available <= capacity:
                    returnCourses.append(course)
                elif comp == ">=" and course.capacity_available >= capacity:
                    returnCourses.append(course)

        return returnCourses

    def byLectureHours(self, courses, hours, comp="="):
        """
        Filter the passed array of courses by passed number of lecture hours using the provided comparison

        Args:
            courses(list<Course>): An array of Course data.
            hours: (float): The number of hours of lecture
            [comp]: (string): How to compare the hours (one of =,<,>), defaults to =

        Raises:
            ValueError (Exception): If hours is negative or comp is invalid

        Returns:
            (list): A list of courses with matching lecture hours
        """
        returnCourses = []
        comparisons = ["=", "<", ">", ">=", "<="]

        if type(hours) != float:
            raise ValueError("Hours must be a floating point number")

        if hours < 0:
            raise ValueError("Hours must not be negative")

        if comp not in comparisons:
            raise ValueError(f"Comparison must be one of {comparisons}")

        for course in courses:
            if comp == "=" and course.lecture_hours == hours:
                returnCourses.append(course)
            elif comp == ">" and course.lecture_hours > hours:
                returnCourses.append(course)
            elif comp == "<" and course.lecture_hours < hours:
                returnCourses.append(course)
            elif comp == ">=" and course.lecture_hours >= hours:
                returnCourses.append(course)
            elif comp == "<=" and course.lecture_hours <= hours:
                returnCourses.append(course)

        return returnCourses

    def byLabHours(self, courses, hours, comp="="):
        """
        Filter the passed array of courses by passed number of lab hours using the provided comparison

        Args:
            courses(list<Course>): An array of Course data.
            hours: (float): The number of hours of lab
            [comp]: (string): How to compare the hours (one of =,<,>)

        Raises:
            ValueError (Exception): If hours is negative or comp is invalid

        Returns:
            (list): A list of courses with matching lab hours
        """
        returnCourses = []
        comparisons = ["=", "<", ">", ">=", "<="]

        if type(hours) != float:
            raise ValueError("Hours must be a floating point number")

        if hours < 0:
            raise ValueError("Hours must not be negative")

        if comp not in comparisons:
            raise ValueError(f"Comparison must be one of {comparisons}")

        for course in courses:
            if comp == "=" and course.lab_hours == hours:
                returnCourses.append(course)
            elif comp == ">" and course.lab_hours > hours:
                returnCourses.append(course)
            elif comp == "<" and course.lab_hours < hours:
                returnCourses.append(course)
            elif comp == ">=" and course.lab_hours >= hours:
                returnCourses.append(course)
            elif comp == "<=" and course.lab_hours <= hours:
                returnCourses.append(course)

        return returnCourses

    def byOffered(self, courses, offered, comparison):
        """
        Filter the passed array of courses by if they are offered based on WebAdvisor data

        Args:
            courses(list<Course>): An array of Course data.
            offered: (boolean): True returns offered courses, false returns unoffered courses

        Raises:
            ValueError (Exception): If offered is not a boolean

        Returns:
            (list): A list of courses that are either offered or unoffered
        """
        returnCourses = []

        if type(offered) != bool:
            raise ValueError("Offered must be a boolean")

        for course in courses:
            course_offered = hasattr(course, "capacity_available") and hasattr(course, "capacity_max")

            if offered and course_offered:
                returnCourses.append(course)
            elif not offered and not course_offered:
                returnCourses.append(course)

        return returnCourses

    def getPrerequisiteTree(self, courses, course_id, comparison):
        """
        Returns all prerequisites of a course with the provided course_id. Prerequisites and the
        root course are found by searching the passed courses array.

        Args:
            courses(list<Course>):  An array of Course data.
            course_id: (string):    Id of root course in the form <code>*<number> (eg. CIS*2750)
            comparison: Unused argument but is needed by Descriptr._perform_search()

        Raises:
            Exception:  If root course cannot be found in courses array

        Returns:
            (dictionary):   A tree of dictionaries, where each node contains:
                            - course (string|Course):       The course object for the root dict and if the course id
                                                            for a prerequisite exists in the courses array, otherwise
                                                            the course id string
                            - prerequisites (list<dict>):   Array of child nodes
        """
        # Find root course in array
        root_course = None
        for c in courses:
            if c.fullname() == course_id.upper():
                root_course = c
                break

        # Raise exception if course does not exist
        if root_course is None:
            raise Exception("Course Not Found")

        # Return course instance and its recursively-found prerequisites
        root_prerequisites = []
        if hasattr(root_course, 'prerequisites'):
            root_prerequisites = root_course.prerequisites.get("simple", [])

        return {
            'course': root_course,
            'prerequisites': self._recursivePrereqSearch(root_prerequisites, courses)
        }

    def _recursivePrereqSearch(self, prerequisites, courses):
        """
            Recursively builds a tree of course prerequisites

            Args:
                prerequisites(list<string>): List of prerequisite course ids
                courses(list<Course>):  An array of Course data.

            Returns:
                (list<dictionary>): An array of dictionary trees (tree structure described in getPrerequisiteTree())
        """

        # Break if no more children
        if len(prerequisites) == 0:
            return prerequisites

        # Else find child prerequisites of each prerequisite
        else:
            result_prerequisites = []
            for child_course_id in prerequisites:

                # Find child course in courses array
                child_course = None
                for c in courses:
                    if c.fullname() == child_course_id:
                        child_course = c
                        break

                # Append node with course_id and empty array if child_course is not found in courses array
                if child_course is None:
                    result_prerequisites.append({
                        'course': child_course_id,
                        'prerequisites': []
                    })

                # Else, find grandchild prerequisites
                else:
                    child_prerequisites = []
                    if hasattr(child_course, 'prerequisites'):
                        child_prerequisites = child_course.prerequisites.get("simple", [])

                    result_prerequisites.append({
                        'course': child_course,
                        'prerequisites': self._recursivePrereqSearch(child_prerequisites, courses)
                    })

            return result_prerequisites
