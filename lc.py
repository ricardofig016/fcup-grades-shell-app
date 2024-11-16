data = [
    {"name": "Test 1", "grade": "?", "maxGrade": 20},
    {"name": "Test 2", "grade": "?", "maxGrade": 20},
]


def get_final_grade():
    min_final = 0
    max_final = 0
    for c in data:
        if c["grade"] != "?":
            min_final += c["grade"] * 0.5
            max_final += c["maxGrade"] * 0.5
    min_final = round(min_final, 1)
    max_final = round(max_final, 1)
    return f"{min_final} / {max_final}"


def get_all_grades():
    string = ""
    for c in data:
        string += f"\t{c['name']}: {c['grade']} / {c['maxGrade']}\n"
    return string
