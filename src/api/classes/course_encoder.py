import json
from json import JSONEncoder
from classes.course import Course


class CourseEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Course):
            return json.dumps({
                "subject":                  o.subject if hasattr(o, "subject") else None,
                "departments":              o.departments if hasattr(o, "departments") else [],
                "code":                     o.code if hasattr(o, "code") else None,
                "number":                   o.number if hasattr(o, "number") else None,
                "name":                     o.name if hasattr(o, "name") else None,
                "semesters_offered":        [semester_offered.name for semester_offered in o.semesters_offered] if hasattr(o, "semesters_offered") else [],
                "lecture_hours":            o.lecture_hours if hasattr(o, "lecture_hours") else None,
                "lab_hours":                o.lab_hours if hasattr(o, "lab_hours") else None,
                "credits":                  o.credits if hasattr(o, "credits") else None,
                "description":              o.description if hasattr(o, "description") else None,
                "distance_education":       o.distance_education.value if hasattr(o, "distance_education") else None,
                "year_parity_restrictions": o.year_parity_restrictions.value if hasattr(o, "year_parity_restrictions") else None,
                "other":                    o.other if hasattr(o, "other") else None,
                "prerequisites":            o.prerequisites if hasattr(o, "prerequisites") else [],
                "equates":                  o.equates if hasattr(o, "equates") else None,
                "corequisites":             o.corequisites if hasattr(o, "corequisites") else None,
                "restrictions":             o.restrictions if hasattr(o, "restrictions") else [],
                "capacity_available":       o.capacity_available if hasattr(o, "capacity_available") else 0,
                "capacity_max":             o.capacity_max if hasattr(o, "capacity_max") else 0,
                "is_full":                  o.is_full(),
                "fullname":                 o.fullname()
            })
        else:
            return super.default(self, o)
