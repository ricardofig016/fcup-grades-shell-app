import json
from icecream import ic

from comp import (
    get_final_grade as comp_get_final_grade,
    get_all_grades as comp_get_all_grades,
)
from lc import (
    get_final_grade as lc_get_final_grade,
    get_all_grades as lc_get_all_grades,
)
from pc import (
    get_final_grade as pc_get_final_grade,
    get_all_grades as pc_get_all_grades,
)
from rc import (
    get_final_grade as rc_get_final_grade,
    get_all_grades as rc_get_all_grades,
)
from tw import (
    get_final_grade as tw_get_final_grade,
    get_all_grades as tw_get_all_grades,
)

grade_functions = {
    "comp": [comp_get_final_grade, comp_get_all_grades],
    "lc": [lc_get_final_grade, lc_get_all_grades],
    "pc": [pc_get_final_grade, pc_get_all_grades],
    "rc": [rc_get_final_grade, rc_get_all_grades],
    "tw": [tw_get_final_grade, tw_get_all_grades],
}


def get_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return data


def get_course_by_name(query, data):
    for course in data:
        for name in course["names"]:
            if name.lower() == query:
                return course
    return None


def get_final_grade(course):
    if course["module_name"] in grade_functions:
        return grade_functions[course["module_name"]][0]()


def get_all_grades(course):
    if course["module_name"] in grade_functions:
        return grade_functions[course["module_name"]][1]()


def shell():
    data = get_data()
    while True:
        try:
            commandStr = input("> ")
        except KeyboardInterrupt:
            commandStr = "exit"

        commandStr = commandStr.strip().lower()
        command = commandStr.split(" ")

        if not command[0]:
            continue

        if command[0] in ["exit", "quit", "q"]:
            print("Exiting shell...")
            break

        # > help
        elif command[0] == "help":
            print("Available commands:")
            print("  courses - list all courses")
            print("  course <course_name> - show course details")
            print("  grades - show all grades for all courses")
            print("  grades <course_name> - show all grades for a course")
            print("  final all - show final grade for all courses")
            print("  final <course_name> - show final grade for a course")
            print("  exit - exit the shell")

        # > courses
        elif command[0] == "courses":
            for course in data:
                print(course["names"][0])

        # > course <course_name>
        elif command[0] == "course":
            try:
                course = get_course_by_name(command[1], data)
                if not course:
                    print(f"Course {command[1]} not found.")
                else:
                    ic(course)
            except IndexError:
                print("Invalid command. Usage: course <course_name>")

        elif command[0] == "grades":
            # > grades
            if len(command) == 1:
                for course in data:
                    print(course["names"][0] + ":")
                    print(get_all_grades(course))

            # > grades <course_name>
            else:
                course = get_course_by_name(command[1], data)
                if not course:
                    print(f"Course {command[1]} not found.")
                else:
                    print(course["names"][0] + ":")
                    print(get_all_grades(course))

        elif command[0] == "final":
            # > final all
            if len(command) == 2 and command[1] == "all":
                for course in data:
                    print(f"{course['names'][0]}: {get_final_grade(course)}")
            # > final <course_name>
            elif len(command) == 2:
                course = get_course_by_name(command[1], data)
                if not course:
                    print(f"Course {command[1]} not found.")
                else:
                    print(f"{course['names'][0]}: {get_final_grade(course)}")

        else:
            print("Invalid command. Use 'help' to see available commands.")


if __name__ == "__main__":
    shell()
