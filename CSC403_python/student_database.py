
class Student:
    students = []

    def __init__(self):
        self.first_name = ""
        self.middle_name = ""
        self.last_name = ""
        self.faculty = ""
        self.department = ""
        self.matric = 0
        self.cgpa = 0.0

    # Add student
    @staticmethod
    def add_student():
        student = Student()

        student.first_name = input("Enter first name: ")
        student.middle_name = input("Enter middle name: ")
        student.last_name = input("Enter last name: ")
        student.faculty = input("Enter faculty: ")
        student.department = input("Enter department: ")
        student.matric = int(input("Enter matric: "))
        student.cgpa = float(input("Enter cgpa: "))

        Student.students.append(student)

        print("Student has been created successfully✅.")

    # underline
    @staticmethod
    def underline():
        length = 130
        print("_" * length)

    # Layout database display
    @staticmethod
    def database_layout():
        serial_no = 1
        spacing = 25

        print("S/N  ", end="")
        print(f"{'Name':<{spacing+10}}"
              f"{'Matric .No':<{spacing}}"
              f"{'CGPA':<{spacing-10}}"
              f"{'Department':<{spacing}}"
              f"Faculty")

        Student.underline()

        for student in Student.students:
            full_name = (
                student.first_name + " " +
                student.middle_name + " " +
                student.last_name
            )

            print(f"{serial_no}.   ", end="")
            print(f"{full_name:<{spacing+10}}"
                  f"{student.matric:<{spacing}}"
                  f"{student.cgpa:<{spacing-10}}"
                  f"{student.department:<{spacing}}"
                  f"{student.faculty}")
            serial_no += 1

        print()

    # Display all students
    @staticmethod
    def display_all_students():
        print()
        if len(Student.students) == 0:
            print("Database is empty!")
        else:
            Student.database_layout()

    # Delete student
    @staticmethod
    def delete_student(matric):
        target = None

        for student in Student.students:
            if student.matric == matric:
                target = student
                break

        answer = input(
            "Are you sure you want to delete this student(Operation can NOT be reversed)?\n yes / no: "
        )

        if target and answer == "yes":
            Student.students.remove(target)
            print(f"Matric number {matric} has been erased successfully")
        else:
            print(f"Matric number {matric} does not exist")

    # Open database (main program loop)
    @staticmethod
    def open_database():
        print("\nOpening database ...\n")

        operation = 0

        while operation != 4:
            print(" Operations:")
            print(" |1. Create student  |  2. View database")
            print(" |3. Delete Student  |  4. Exit")
            operation = int(input(" Select(1-4): "))

            if operation == 1:
                Student.add_student()

            elif operation == 2:
                Student.display_all_students()

            elif operation == 3:
                matric = int(input("Enter matric number to delete: "))
                Student.delete_student(matric)

            elif operation == 4:
                print("Exiting database...")

            else:
                print("ERROR: Invalid option!")
                
                
        print("Database closed.\n")
        

Student.open_database()

        