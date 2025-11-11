import mysql.connector as con


def connect_to_database():
    try:
        mycon = con.connect(
            host="localhost",
            user="newuser",
            passwd="Shambhuraj@007",
            database="employee_db"
        )
        return mycon
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employee (
            SSN VARCHAR(20) PRIMARY KEY,
            Ename VARCHAR(255),
            state VARCHAR(50),
            salary DECIMAL(10, 2)
        )
    ''')
    print("Employee table created successfully!")


def insert_employee(conn, cursor, ssn, ename, state, salary):
    try:
        cursor.execute(
            "INSERT INTO Employee (SSN, Ename, state, salary) VALUES (%s, %s, %s, %s)",
            (ssn, ename, state, salary)
        )
        conn.commit()
        print("Employee added successfully!")
    except Exception as e:
        print(f"Failed to add employee: {e}")


def retrieve_by_ssn(cursor, ssn):
    try:
        cursor.execute("SELECT * FROM Employee WHERE SSN=%s", (ssn,))
        employee = cursor.fetchone()
        if employee:
            print(f"SSN: {employee[0]} | Name: {employee[1]} | State: {employee[2]} | Salary: {employee[3]}")
        else:
            print("Employee not found.")
    except Exception as e:
        print(f"Failed to retrieve employee: {e}")


def update_state_mh_to_tn(conn, cursor):
    try:
        cursor.execute("UPDATE Employee SET state='TN' WHERE state='MH'")
        conn.commit()
        if cursor.rowcount > 0:
            print(f"{cursor.rowcount} employee(s) updated from MH to TN successfully!")
        else:
            print("No employees found with state 'MH'.")
    except Exception as e:
        print(f"Failed to update state: {e}")


def delete_employees_from_state(conn, cursor, state):
    try:
        cursor.execute("DELETE FROM Employee WHERE state=%s", (state,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"{cursor.rowcount} employee(s) from {state} deleted successfully!")
        else:
            print(f"No employees found from {state}.")
    except Exception as e:
        print(f"Failed to delete employees: {e}")


def view_all_employees(cursor):
    try:
        cursor.execute("SELECT * FROM Employee")
        employees = cursor.fetchall()
        if not employees:
            print("No employees found.")
        else:
            print("\n--- All Employees ---")
            for emp in employees:
                print(f"SSN: {emp[0]} | Name: {emp[1]} | State: {emp[2]} | Salary: {emp[3]}")
    except Exception as e:
        print(f"Failed to fetch employees: {e}")


def menu(conn, cursor):
    while True:
        print("\n===== Employee Management System =====")
        print("1. Insert Employee Record")
        print("2. Retrieve Employee by SSN")
        print("3. View All Employees")
        print("4. Update State (MH to TN)")
        print("5. Delete Employees from Gujarat")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            ssn = input("Enter SSN: ").strip()
            ename = input("Enter Employee Name: ").strip()
            state = input("Enter State: ").strip()
            salary = input("Enter Salary: ").strip()
            try:
                salary = float(salary)
                insert_employee(conn, cursor, ssn, ename, state, salary)
            except ValueError:
                print("Invalid salary. Please enter a numeric value.")

        elif choice == '2':
            ssn = input("Enter SSN to retrieve: ").strip()
            retrieve_by_ssn(cursor, ssn)

        elif choice == '3':
            view_all_employees(cursor)

        elif choice == '4':
            update_state_mh_to_tn(conn, cursor)

        elif choice == '5':
            delete_employees_from_state(conn, cursor, "Gujarat")

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    mycon = connect_to_database()
    if mycon:
        cursor = mycon.cursor()
        create_tables(cursor)
        menu(mycon, cursor)
        cursor.close()
        mycon.close()
    else:
        print("Failed to connect to the database. Exiting...")
