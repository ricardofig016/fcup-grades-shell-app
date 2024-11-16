data = [
    {"name": "Test 1", "grade": 18.5, "maxGrade": 20},
    {"name": "Test 2", "grade": "?", "maxGrade": 20},
    {"name": "Project Part 1", "grade": 18.2, "maxGrade": 20},
    {"name": "Project Part 2", "grade": "?", "maxGrade": 20},
]


def get_final_grade():
    min_final = 0
    max_final = 0
    for c in data:
        if c["name"] == "Test 1":
            mult = 0.2
        elif c["name"] == "Test 2":
            mult = 0.4
        elif c["name"] == "Project Part 1":
            mult = 0.15
        elif c["name"] == "Project Part 2":
            mult = 0.25
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
