from pymongo import MongoClient
from bson.code import Code


def connect_to_database():
    try:
        client = MongoClient('localhost', 27017)
        db = client['library_database']
        collection = db['Books']
        print("Connected to MongoDB successfully!")
        return client, db, collection
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None, None, None


def insert_book(collection, name, pages):
    try:
        book_doc = {
            "Name": name,
            "Pages": pages
        }
        result = collection.insert_one(book_doc)
        print(f"Book added successfully! Document ID: {result.inserted_id}")
    except Exception as e:
        print(f"Failed to insert book: {e}")


def categorize_books_mapreduce(collection):
    try:
        # Map function: Categorize books based on page count
        map_function = Code("""
            function() {
                var category;
                if (this.Pages > 300) {
                    category = "Big book";
                } else {
                    category = "Small book";
                }
                emit(category, {
                    name: this.Name,
                    pages: this.Pages
                });
            }
        """)
        
        # Reduce function: Collect all books in each category
        reduce_function = Code("""
            function(key, values) {
                var books = [];
                values.forEach(function(value) {
                    books.push({
                        name: value.name,
                        pages: value.pages
                    });
                });
                return { books: books };
            }
        """)
        
        # Execute MapReduce
        result = collection.map_reduce(
            map_function,
            reduce_function,
            "book_categories"
        )
        
        print("\n--- MapReduce Operation Completed ---")
        print(f"Results stored in collection: {result.full_name}")
        
        # Display results
        display_mapreduce_results(result)
        
    except Exception as e:
        print(f"Failed to perform MapReduce: {e}")


def display_mapreduce_results(result_collection):
    try:
        print("\n--- Book Categorization Results ---")
        for doc in result_collection.find():
            category = doc['_id']
            print(f"\nCategory: {category}")
            
            # Handle both single book and multiple books cases
            if 'books' in doc['value']:
                books = doc['value']['books']
                if isinstance(books, list):
                    for book in books:
                        print(f"  - {book['name']} ({book['pages']} pages)")
                else:
                    print(f"  - {books['name']} ({books['pages']} pages)")
            else:
                print(f"  - {doc['value']['name']} ({doc['value']['pages']} pages)")
                
    except Exception as e:
        print(f"Failed to display results: {e}")


def view_all_books(collection):
    try:
        books = collection.find()
        book_list = list(books)
        if not book_list:
            print("No books found in the collection.")
        else:
            print("\n--- All Books ---")
            for book in book_list:
                print(f"Name: {book['Name']} | Pages: {book['Pages']}")
    except Exception as e:
        print(f"Failed to fetch books: {e}")


def insert_sample_data(collection):
    """Insert sample books for testing"""
    try:
        sample_books = [
            {"Name": "Understanding MongoDB", "Pages": 200},
            {"Name": "Python Programming", "Pages": 450},
            {"Name": "Data Structures", "Pages": 350},
            {"Name": "Web Development Basics", "Pages": 180},
            {"Name": "Advanced Algorithms", "Pages": 520},
            {"Name": "MongoDB Guide", "Pages": 250},
            {"Name": "Introduction to Python", "Pages": 150},
            {"Name": "Database Systems", "Pages": 600}
        ]
        
        result = collection.insert_many(sample_books)
        print(f"{len(result.inserted_ids)} sample books inserted successfully!")
    except Exception as e:
        print(f"Failed to insert sample data: {e}")


def menu(collection, db):
    while True:
        print("\n===== Book Categorization System (MapReduce) =====")
        print("1. Insert Book")
        print("2. View All Books")
        print("3. Insert Sample Data")
        print("4. Perform MapReduce (Categorize Books)")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter Book Name: ").strip()
            pages = input("Enter Number of Pages: ").strip()
            
            try:
                pages = int(pages)
                insert_book(collection, name, pages)
            except ValueError:
                print("Invalid input. Pages must be a numeric value.")

        elif choice == '2':
            view_all_books(collection)

        elif choice == '3':
            insert_sample_data(collection)

        elif choice == '4':
            categorize_books_mapreduce(collection)

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    client, db, collection = connect_to_database()
    if collection is not None:
        menu(collection, db)
        client.close()
        print("MongoDB connection closed.")
    else:
        print("Failed to connect to MongoDB. Exiting...")