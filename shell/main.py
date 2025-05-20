import json
import os
from icecream import ic


def get_data():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(curr_dir) == "grades":
        curr_dir = os.path.join(curr_dir, "shell")
    data_path = os.path.join(curr_dir, "data.json")
    with open(data_path, "r") as file:
        data = json.load(file)
    return data


def get_course_by_name(query, data):
    for course in data:
        for name in course["names"]:
            if name.lower() == query:
                return course
    return None


def get_final_grade(course):
    min_final = 0
    max_final = 0
    for c in course["components"]:
        if c["grade"] != "?":
            min_final += c["grade"] * c["weight"]
            max_final += 20 * c["weight"]
    min_final = round(min_final, 1)
    max_final = round(max_final, 1)
    perc = round(min_final * 100 / max_final, 1) if max_final != 0 else 0
    return f"{min_final} / {max_final} ({perc}%)"


def get_all_grades(course):
    string = ""
    for c in course["components"]:
        if c["grade"] != "?":
            string += f"\t{c['name']}: {c['grade']} / 20\n"
    return string


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
                    grades_string = get_all_grades(course)
                    if grades_string:
                        print(course["names"][0] + ":")
                        print(grades_string)

            # > grades <course_name>
            else:
                course = get_course_by_name(command[1], data)
                if not course:
                    print(f"Course {command[1]} not found.")
                else:
                    grades_string = get_all_grades(course)
                    if grades_string:
                        print(course["names"][0] + ":")
                        print(grades_string)
                    else:
                        print(f"No grades available for {course["names"][0]}")

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
                print("Invalid command. Usage: final all | final <course_name>")

        else:
            print("Invalid command. Use 'help' to see available commands.")


if __name__ == "__main__":
    shell()
