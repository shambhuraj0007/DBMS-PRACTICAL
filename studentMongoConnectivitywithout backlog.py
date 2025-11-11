import pymongo

def insertData(name, roll_no, email, marks, age):
    stud_collection.insert_one({
        "Name": name,
        "Roll_no": roll_no,
        "Email": email,
        "Marks": marks,
        "Age": age
    })

def displayData():
    data = stud_collection.find()
    for d in data:
        print(d)

def displayDataById(roll_no):
    data = stud_collection.find({'Roll_no': roll_no})
    result = []
    for d in data:
        result.append(d)
    return result

def updateData(prev, nextt): 
    stud_collection.update_one(prev, nextt)

def deleteData(roll_no): 
    stud_collection.delete_one({'Roll_no': roll_no})

if __name__ == "__main__":
    print("Welcome to MongoDB CRUD Application...")
    client = pymongo.MongoClient("mongodb://localhost:27017/") 
    print("Connected to:", client)
    
    db = client['TECO2526A025'] 
    stud_collection = db['student'] 
    
    while True:
        print("\n***** Menu *****") 
        print("1. Insert Data")
        print("2. Update Data")
        print("3. Delete Data")
        print("4. Display All Data") 
        print("5. Search by Roll No")
        print("6. Exit")

        
        choice = int(input("Enter your choice: "))  
        
        if choice == 1:
            name = input("Enter Name: ")
            roll_no = int(input("Enter Roll No: ")) 
            email = input("Enter Email: ")
            marks = int(input("Enter Marks: "))
            age = int(input("Enter Age: "))
            insertData(name, roll_no, email, marks, age) 
            print("Record Inserted Successfully")

        elif choice == 2:
            roll_no = int(input("Enter Roll No to Update: ")) 
            data = displayDataById(roll_no)
            if not data:
                print("No Record Found to Update")
                continue
            print("Current Data:")
            for d in data:
                print(d)
            name = input("Enter New Name: ")
            email = input("Enter New Email: ")
            marks = int(input("Enter New Marks: ")) 
            age = int(input("Enter New Age: "))
            prev = {"Roll_no": roll_no}
            nextt = {"$set": {"Name": name, "Email": email, "Marks": marks, "Age": age}}
            updateData(prev, nextt)
            print("Record Updated Successfully")

        elif choice == 3:
            roll_no = int(input("Enter Roll No to Delete: ")) 
            data = displayDataById(roll_no)
            if not data:
                print("No Record Found to Delete")
                continue
            deleteData(roll_no)
            print("Record Deleted Successfully")

        elif choice == 4:
            print("\nAll Records:")
            displayData()

        elif choice == 5:
            roll_no = int(input("Enter Roll No to Search: ")) 
            data = displayDataById(roll_no)
            if not data:
                print("No Record Found")
            else:
                print("Record Found:")
                for d in data:
                    print(d)

        elif choice == 6:
            print("Program Ended. Goodbye!")
            break

        else:
            print("Invalid Choice. Try again.")