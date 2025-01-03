evalComponents = [
    {
        "name": "Problem Set 1",
        "item": "Submitted Implementations",
        "grade": 100,
        "maxGrade": 100,
    },
    {
        "name": "Problem Set 2",
        "item": "Submitted Implementations",
        "grade": 100,
        "maxGrade": 100,
    },
    {
        "name": "Problem Set 3",
        "item": "Submitted Implementations",
        "grade": 45,
        "maxGrade": 100,
    },
    {
        "name": "Problem Set 4",
        "item": "Submitted Implementations",
        "grade": 85,
        "maxGrade": 100,
    },
    {
        "name": "Problem Set 5",
        "item": "Submitted Implementations",
        "grade": 85,  # not verified
        "maxGrade": 100,
    },
    {
        "name": "Problem Set 6",
        "item": "Submitted Implementations",
        "grade": 79,  # not verified
        "maxGrade": 100,
    },
    {
        "name": "Problem Set 7",
        "item": "Submitted Implementations",
        "grade": 73,  # not verified
        "maxGrade": 100,
    },
    {
        "name": "Problem Set 8",
        "item": "Submitted Implementations",
        "grade": "?",
        "maxGrade": 100,
    },
    {
        "name": "Problem Set 9",
        "item": "Submitted Implementations",
        "grade": "?",
        "maxGrade": 100,
    },
    {
        "name": "Problem Set 10",
        "item": "Submitted Implementations",
        "grade": "?",
        "maxGrade": 100,
    },
    {
        "name": "Contest 1",
        "item": "Competitive Events",
        "grade": 80,
        "maxGrade": 100,
    },
    {
        "name": "Contest 2",
        "item": "Competitive Events",
        "grade": 77,
        "maxGrade": 100,
    },
    {
        "name": "Contest 3",
        "item": "Competitive Events",
        "grade": "?",
        "maxGrade": 100,
    },
    {
        "name": "Creating a Problem",
        "item": "Presentations and Class Participation",
        "grade": "?",
        "maxGrade": 100,
    },
    {
        "name": "Presenting a Problem",
        "item": "Presentations and Class Participation",
        "grade": "?",
        "maxGrade": 100,
    },
    {
        "name": "Global Effort",
        "item": "Presentations and Class Participation",
        "grade": "?",
        "maxGrade": 100,
    },
]


def get_final_grade():
    min_si = 0
    max_si = 0
    min_ce = 0
    max_ce = 0
    min_pp = 0
    max_pp = 0
    for component in evalComponents:
        # submitted implementations
        if component["item"] == "Submitted Implementations":
            if component["grade"] != "?":
                min_si += component["grade"] * 0.12
                max_si += component["maxGrade"] * 0.12
        # competitive events
        elif component["item"] == "Competitive Events":
            if "3" in component["name"]:
                mult = 0.5
            else:
                mult = 0.25
            if component["grade"] != "?":
                min_ce += component["grade"] * mult
                max_ce += component["maxGrade"] * mult
        # presentations and class participation
        elif component["item"] == "Presentations and Class Participation":
            if component["name"] == "Creating a Problem":
                mult = 0.4
            elif component["name"] == "Presenting a Problem":
                mult = 0.3
            elif component["name"] == "Global Effort":
                mult = 0.3
            if component["grade"] != "?":
                min_pp += component["grade"] * mult
                max_pp += component["maxGrade"] * mult
    min_si = min(min_si, 100)
    max_si = min(max_si, 100)
    # final grade
    min_final = round((min_si * 0.5 + min_ce * 0.3 + min_pp * 0.2) / 5, 1)
    max_final = round((max_si * 0.5 + max_ce * 0.3 + max_pp * 0.2) / 5, 1)
    perc = round(min_final * 100 / max_final, 1)
    return f"{min_final} / {max_final} ({perc}%)"


def get_all_grades():
    string = ""
    for c in evalComponents:
        string += f"\t{c['name']}: {c['grade']} / {c['maxGrade']}\n"
    return string
