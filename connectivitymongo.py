from pymongo import MongoClient


def connect_to_database():
    try:
        # Connect to MongoDB (default port 27017)
        client = MongoClient('localhost', 27017)
        db = client['student_database']  # Create/access database
        collection = db['student']  # Create/access collection
        print("Connected to MongoDB successfully!")
        return client, db, collection
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None, None, None


def insert_student(collection, roll_no, s_name, semester, year, no_of_backlogs):
    try:
        student_doc = {
            "Roll_no": roll_no,
            "S_name": s_name,
            "Semester": semester,
            "Year": year,
            "No_of_backlogs": no_of_backlogs
        }
        result = collection.insert_one(student_doc)
        print(f"Student added successfully! Document ID: {result.inserted_id}")
    except Exception as e:
        print(f"Failed to insert student: {e}")


def delete_students_with_backlogs(collection, backlog_threshold=4):
    try:
        # Delete students with backlogs greater than 4
        result = collection.delete_many({"No_of_backlogs": {"$gt": backlog_threshold}})
        if result.deleted_count > 0:
            print(f"{result.deleted_count} student(s) with backlogs > {backlog_threshold} deleted successfully!")
        else:
            print(f"No students found with backlogs > {backlog_threshold}.")
    except Exception as e:
        print(f"Failed to delete students: {e}")


def retrieve_by_roll_no(collection, roll_no):
    try:
        student = collection.find_one({"Roll_no": roll_no})
        if student:
            print("\n--- Student Details ---")
            print(f"Roll No: {student['Roll_no']}")
            print(f"Name: {student['S_name']}")
            print(f"Semester: {student['Semester']}")
            print(f"Year: {student['Year']}")
            print(f"No of Backlogs: {student['No_of_backlogs']}")
        else:
            print("Student not found.")
    except Exception as e:
        print(f"Failed to retrieve student: {e}")


def view_all_students(collection):
    try:
        students = collection.find()
        student_list = list(students)
        if not student_list:
            print("No students found in the collection.")
        else:
            print("\n--- All Students ---")
            for student in student_list:
                print(f"Roll No: {student['Roll_no']} | Name: {student['S_name']} | "
                      f"Semester: {student['Semester']} | Year: {student['Year']} | "
                      f"Backlogs: {student['No_of_backlogs']}")
    except Exception as e:
        print(f"Failed to fetch students: {e}")


def menu(collection):
    while True:
        print("\n===== Student Management System (MongoDB) =====")
        print("1. Insert Student Document")
        print("2. View All Students")
        print("3. Retrieve Student by Roll No")
        print("4. Delete Students with Backlogs > 4")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            roll_no = input("Enter Roll No: ").strip()
            s_name = input("Enter Student Name: ").strip()
            semester = input("Enter Semester: ").strip()
            year = input("Enter Year: ").strip()
            no_of_backlogs = input("Enter Number of Backlogs: ").strip()
            
            try:
                semester = int(semester)
                year = int(year)
                no_of_backlogs = int(no_of_backlogs)
                insert_student(collection, roll_no, s_name, semester, year, no_of_backlogs)
            except ValueError:
                print("Invalid input. Semester, Year, and Backlogs must be numeric values.")

        elif choice == '2':
            view_all_students(collection)

        elif choice == '3':
            roll_no = input("Enter Roll No to retrieve: ").strip()
            retrieve_by_roll_no(collection, roll_no)

        elif choice == '4':
            delete_students_with_backlogs(collection, 4)

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    client, db, collection = connect_to_database()
    if collection is not None:
        menu(collection)
        client.close()
        print("MongoDB connection closed.")
    else:
        print("Failed to connect to MongoDB. Exiting...")
