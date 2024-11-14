import json
from icecream import ic


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


def get_grade(course):
    string = course["names"][0]


def get_all_grades(data):
    grades = []
    if not "evalComponents" in data:
        return []
    for component in data["evalComponents"]:
        if "grade" in component:
            grades.append(
                f"{component["name"]}: {component["grade"]} / {component["maxGrade"]}"
            )
        else:
            grades += get_all_grades(component)
    return grades


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
            print("  grades - show calculated grades for all courses")
            print("  grades <course_name> - show grades for a course")
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
                    print(get_grade(course))

            # > grades <course_name>
            else:
                course = get_course_by_name(command[1], data)
                if not course:
                    print(f"Course {command[1]} not found.")
                else:
                    ic(get_all_grades(course))

        else:
            print("Invalid command. Use 'help' to see available commands.")


if __name__ == "__main__":
    shell()
