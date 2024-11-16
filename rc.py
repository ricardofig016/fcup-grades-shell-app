data = [
    {"name": "Test 1", "grade": 15.8, "maxGrade": 20},
    {"name": "Test 2", "grade": "?", "maxGrade": 20},
    {"name": "Test 3", "grade": "?", "maxGrade": 20},
    {"name": "Project", "grade": "?", "maxGrade": 20},
]


def get_final_grade():
    min_final = 0
    max_final = 0
    for c in data:
        if "Test" in c["name"]:
            mult = 0.3
        else:
            mult = 0.1
        if c["grade"] != "?":
            min_final += c["grade"] * mult
            max_final += c["maxGrade"] * mult
    min_final = round(min_final, 1)
    max_final = round(max_final, 1)
    return f"{min_final} / {max_final}"


def get_all_grades():
    string = ""
    for c in data:
        string += f"\t{c['name']}: {c['grade']} / {c['maxGrade']}\n"
    return string
