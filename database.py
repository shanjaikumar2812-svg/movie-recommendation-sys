from pymongo import MongoClient
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db= client["movies_db"]
    return db
db=get_db()
movies_col = db["movies"]
user_col = db["users"]
ratings_col = db["ratings"]

print("mongoDB connected successfully")
