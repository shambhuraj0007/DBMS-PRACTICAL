import mysql.connector as con


def connect_to_database():
    try:
        mycon = con.connect(
            host="localhost",
            user="newuser",
            passwd="Shambhuraj@007",
            database="doctor_appointments"
        )
        return mycon
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            phone_number VARCHAR(20),
            email VARCHAR(255)
        )
    ''')


def create_patient(conn, cursor, name, phone, email):
    try:
        cursor.execute(
            "INSERT INTO Patients (name, phone_number, email) VALUES (%s, %s, %s)",
            (name, phone, email)
        )
        conn.commit()  # Commit on connection
        print("Patient added successfully!")
    except Exception as e:
        print(f"Failed to add patient: {e}")


def view_patients(cursor):
    try:
        cursor.execute("SELECT * FROM Patients")
        patients = cursor.fetchall()
        if not patients:
            print("No patients found.")
        else:
            for patient in patients:
                print(f"ID: {patient[0]} | Name: {patient[1]} | Phone: {patient[2]} | Email: {patient[3]}")
    except Exception as e:
        print(f"Failed to fetch patients: {e}")


def search_patient(cursor, patient_id):
    try:
        cursor.execute("SELECT * FROM Patients WHERE id=%s", (patient_id,))
        patient = cursor.fetchone()
        if patient:
            print(f"ID: {patient[0]} | Name: {patient[1]} | Phone: {patient[2]} | Email: {patient[3]}")
        else:
            print("Patient not found.")
    except Exception as e:
        print(f"Failed to search patient: {e}")


def update_patient(conn, cursor, patient_id, name, phone, email):
    try:
        cursor.execute(
            "UPDATE Patients SET name=%s, phone_number=%s, email=%s WHERE id=%s",
            (name, phone, email, patient_id)
        )
        conn.commit()  # Commit on connection
        if cursor.rowcount > 0:
            print("Patient updated successfully!")
        else:
            print("Patient not found.")
    except Exception as e:
        print(f"Failed to update patient: {e}")


def delete_patient(conn, cursor, patient_id):
    try:
        cursor.execute("DELETE FROM Patients WHERE id=%s", (patient_id,))
        conn.commit()  # Commit on connection
        if cursor.rowcount > 0:
            print("Patient deleted successfully!")
        else:
            print("Patient not found.")
    except Exception as e:
        print(f"Failed to delete patient: {e}")


def menu(conn, cursor):
    while True:
        print("\nDoctor Appointment Management System")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter patient name: ").strip()
            phone = input("Enter phone number: ").strip()
            email = input("Enter email: ").strip()
            create_patient(conn, cursor, name, phone, email)

        elif choice == '2':
            view_patients(cursor)

        elif choice == '3':
            patient_id = input("Enter patient ID: ").strip()
            if patient_id.isdigit():
                search_patient(cursor, int(patient_id))
            else:
                print("Invalid patient ID. Please enter a numeric value.")

        elif choice == '4':
            patient_id = input("Enter patient ID: ").strip()
            if patient_id.isdigit():
                name = input("Enter new name: ").strip()
                phone = input("Enter new phone number: ").strip()
                email = input("Enter new email: ").strip()
                update_patient(conn, cursor, int(patient_id), name, phone, email)
            else:
                print("Invalid patient ID. Please enter a numeric value.")

        elif choice == '5':
            patient_id = input("Enter patient ID to delete: ").strip()
            if patient_id.isdigit():
                delete_patient(conn, cursor, int(patient_id))
            else:
                print("Invalid patient ID. Please enter a numeric value.")

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "_main_":
    mycon = connect_to_database()
    if mycon:
        cursor = mycon.cursor()
        create_tables(cursor)
        menu(mycon, cursor)
        cursor.close()
        mycon.close()
    else:
        print("Failed to connect to the database. Exiting...")