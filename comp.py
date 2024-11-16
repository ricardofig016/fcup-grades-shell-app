data = [
    {"name": "Exam", "grade": "?", "maxGrade": 20},
    {"name": "Project Part 1", "grade": "?", "maxGrade": 20},
    {"name": "Project Part 2", "grade": "?", "maxGrade": 20},
]


def get_final_grade():
    min_final = 0
    max_final = 0
    for c in data:
        if "Project" in c["name"]:
            mult = 0.15
        else:
            mult = 0.7
        if c["grade"] == "?":
            min_final += 0
            max_final += c["maxGrade"] * mult
        else:
            min_final += c["grade"] * mult
            max_final += c["grade"] * mult
    min_final = round(min_final, 1)
    max_final = round(max_final, 1)
    if min_final == max_final:
        return min_final
    return f"{min_final} - {max_final}"


def get_all_grades():
    string = ""
    for c in data:
        string += f"\t{c['name']}: {c['grade']} / {c['maxGrade']}\n"
    return string
