"""
This file contains helper functions used by the Course class
"""

"""
Convert one long line of text to a bunch of lines of wrapped text at a certain max length
"""
def multi_line_repr(text, max_line_len):
	text = text.replace("\n", " ") #Replace newlines with spaces as we want control of where newlines are printed

	lines = []
	
	curr_line = ""
	curr_line_start = 0
	text_len = len(text)

	while curr_line_start < text_len:
		curr_line_end = min((curr_line_start+max_line_len), text_len)
		
		line_can_be_split = (" " in text[curr_line_start:curr_line_end])
		if line_can_be_split: #If line has spaces it can be split
			while curr_line_end != text_len and (text[curr_line_end] != " "):
				curr_line_end -= 1

		curr_line = text[curr_line_start:curr_line_end]
		lines.append(curr_line)

		curr_line_start = curr_line_end
		if line_can_be_split:
			curr_line_start += 1

	return lines
	
def get_course_representation(course, max_line_length):
	lines = multi_line_repr(course.subject, max_line_length)

	semesters_offered_str = ",".join(semester_offered.name for semester_offered in course.semesters_offered)

	lecture_hours = course.lecture_hours
	if float(course.lecture_hours).is_integer() == True:
		lecture_hours = int(course.lecture_hours)

	lab_hours = course.lab_hours
	if float(course.lab_hours).is_integer() == True:
		lab_hours = int(course.lab_hours)

	course_header = course.code+"*"+course.number+" "+course.name+" "+semesters_offered_str+\
		" ("+str(lecture_hours)+"-"+str(lab_hours)+") ["+str("%.2f" % course.credits)+"]"
	lines += multi_line_repr(course_header, max_line_length)

	after_header_pos = len(lines)

	if course.distance_education.value or course.year_parity_restrictions.value or hasattr(course, "other"):
		offerings = "Offering(s):" 
		if course.distance_education.value:
			offerings += " "+str(course.distance_education.value)
		if course.year_parity_restrictions.value:
			offerings += " "+str(course.year_parity_restrictions.value)
		if hasattr(course, "other"):
			offerings += " "+course.other
		lines += multi_line_repr(offerings, max_line_length)

	if hasattr(course, "prerequisites"):
		original_prerequisites = "Prerequisite(s): "
		original_prerequisites += course.prerequisites["original"]
		lines += multi_line_repr(original_prerequisites, max_line_length)

	if hasattr(course, "equates"):
		equates = "Equate(s): "+course.equates
		lines += multi_line_repr(equates, max_line_length)

	if hasattr(course, "corequisites"):
		corequisites = "Co-requisite(s): "+course.corequisites
		lines += multi_line_repr(corequisites, max_line_length)

	if hasattr(course, "restrictions"):
		for restriction in course.restrictions:
			restriction = ("Restriction(s): "+restriction)
			lines += multi_line_repr(restriction, max_line_length)

	departments = "Department(s): "+(", ".join(department for department in course.departments))
	lines += [departments]

	if hasattr(course, "capacity_available") and hasattr(course, "capacity_max"):
		capacity = "Capacity: " + str(course.capacity_available) + "/" + str(course.capacity_max)
		if course.is_full():
			capacity += " (full)"
		lines += multi_line_repr(capacity, max_line_length)

	#Code to print the above lines. Everything is auto-scaled into a nice display box:
	lines_len = len(lines)
	longest_line_len = len(max(lines, key=len))

	course_description_lines = []
	if hasattr(course, "description"):
		course_description_lines = [""]+multi_line_repr(course.description, longest_line_len)+[""]

	lines = lines[0:after_header_pos] + course_description_lines + lines[after_header_pos:lines_len]

	result = "+"+("-"*(longest_line_len+2))+"+\n"
	for line in lines:
		curr_line_len = len(line)
		result += ("| "+line + (" "*(longest_line_len-curr_line_len))+" |\n")
	result += "+"+("-"*(longest_line_len+2))+"+"

	return result
