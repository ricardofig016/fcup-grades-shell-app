data = [
    {"name": "Test 1", "grade": "?", "weight": 0.3},
    {"name": "Test 2", "grade": "?", "weight": 0.3},
    {"name": "Project", "grade": "?", "weight": 0.4},
]


def get_final_grade():
    min_final = 0
    max_final = 0
    for c in data:
        if c["grade"] != "?":
            min_final += c["grade"] * c["weight"]
            max_final += 20 * c["weight"]
    min_final = round(min_final, 1)
    max_final = round(max_final, 1)
    perc = round(min_final * 100 / max_final, 1) if max_final != 0 else 0
    return f"{min_final} / {max_final} ({perc}%)"


def get_all_grades():
    string = ""
    for c in data:
        string += f"\t{c['name']}: {c['grade']} / 20\n"
    return string
