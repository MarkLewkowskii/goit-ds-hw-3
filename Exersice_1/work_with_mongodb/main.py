from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError  # Importing PyMongoError for exception handling

# Connecting to the database
client = MongoClient(
    "mongodb+srv://marina27043:I2gR3SalxamYUzYG@cluster0.vcftq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

db = client.book

# Fill data
def fill_data(db):
    try:
        result_many = db.cats.insert_many(
        [
            {
                "name": "Lama",
                "age": 2,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Liza",
                "age": 4,
                "features": ["ходить в лоток", "дає себе гладити", "білий"],
            },
            {
                "name": "barsik",
                "age": 3,
                "features": ["ходить в капці", "дає себе гладити", "рудий"],
            },
        ]
    )
        print("Data added")
    except PyMongoError as e:
        print(f"An error occurred while inserting data: {e}")

# Function to read all documents
def read_all_documents(db):
    try:
        result = db.cats.find({})
        for el in result:
            print(el)
    except PyMongoError as e:
        print(f"An error occurred while reading documents: {e}")

# Function to read a document by name
def read_by_name(db, name):
    try:
        return db.cats.find_one({"name": name})
    except PyMongoError as e:
        print(f"An error occurred while reading by name: {e}")
        return None

# Function to update the age of a cat by name
def update_age_by_name(db, age, name):
    try:
        result = db.cats.update_one({"name": name}, {"$set": {"age": age}})
        return result.modified_count
    except PyMongoError as e:
        print(f"An error occurred while updating age: {e}")
        return 0

# Function to add a new feature to the list of features of a cat by name
def add_new_features_by_name(db, name, new_feature):
    try:
        result = db.cats.update_one(
            {"name": name},
            {"$addToSet": {"features": new_feature}}
        )
        return result.modified_count
    except PyMongoError as e:
        print(f"An error occurred while adding a new feature: {e}")
        return 0

# Function to delete a document by name
def delete_by_name(db, name):
    try:
        result = db.cats.delete_one({"name": name})
        return result.deleted_count
    except PyMongoError as e:
        print(f"An error occurred while deleting by name: {e}")
        return 0

# Function to delete all documents
def delete_all_data(db):
    try:
        result = db.cats.delete_many({})
        return result.deleted_count
    except PyMongoError as e:
        print(f"An error occurred while deleting all data: {e}")
        return 0

# Try to use:
# print(read_all_documents(db))
# print(read_by_name(db, "barsik"))
# print(update_age_by_name(db, 5, "barsik"))
# print(add_new_features_by_name(db, "barsik", "любит гратися"))
# print(delete_by_name(db, "barsik"))
# print(delete_all_data(db))
# fill_data(db)
