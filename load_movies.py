import pandas as pd
from database import movies_col, user_col, ratings_col
from datetime import datetime
#clear the existing data
movies_col.delete_many({})
user_col.delete_many({})
ratings_col.delete_many({})
#load the dataset
movies_df = pd.read_csv(r"D:\ml-latest-small\ml-latest-small\movies.csv")
ratings_df = pd.read_csv(r"D:\ml-latest-small\ml-latest-small\ratings.csv")
print(f"Movies found: {len(movies_df)}")
print(f"Ratings found: {len(ratings_df)}")
print(f"Users found: {len(ratings_df['userId'].unique())}")
#procsess movies collection
#cleaning the genres column
movies_df["genres"] =movies_df["genres"].apply(lambda x: x.split('|')
                                                if x != '(no genres listed)' else [])
#extract the year
movies_df["year"] = movies_df["title"].str.extract(r'\((\d{4})\)')
#clean the title
movies_df["title"] = movies_df["title"].str.replace(r'\s*\(\d{4}\)', '',regex=True)
#calculate the user average rating
avg_ratings = ratings_df.groupby("movieId")["rating"].agg(["mean", "count"]).reset_index()
avg_ratings.columns = ["movieId", "avg_rating", "rating_count"]
#merge 
movies_df = movies_df.merge(avg_ratings, on="movieId" ,how="left")
#final polishing
movies_df["avg_rating"] = movies_df["avg_rating"].fillna(0).round(2)
movies_df["rating_count"] = movies_df["rating_count"].fillna(0).astype(int)
#convert to mongodb document
movies_docs=[]
for _,row in movies_df.iterrows():
    movies_docs.append({
        "movie_Id" : int(row["movieId"]),
        "title" : row["title"].strip(),
        "genres" : row["genres"],
        "year" : int(row["year"]) if pd.notnull(row["year"]) else "unknown",
        "avg_rating" : float(row["avg_rating"]),
        "rating_count" : int(row["rating_count"])
    })
movies_col.insert_many(movies_docs)
print(f"Inserted {len(movies_docs)} movies into database")
#user status and creation
user_ids = ratings_df["userId"].unique()
#get user status
user_status = ratings_df.groupby("userId").agg(
    total_ratings = ("rating", "count"),
    avg_rating = ("rating", "mean"),
    max_rating = ("rating", "max"),
    min_rating = ("rating", "min")
).reset_index()
user_docs =[]
for _, row in user_status.iterrows():
    user_docs.append({
        "user_id" : int(row["userId"]),
        "name" :f"User_{int(row["userId"])}",
        "total_ratings" : int(row["total_ratings"]),
        "avg_rating_given" : round(float(row["avg_rating"]), 2),
        "max_rating" : float(row["max_rating"]),
        "min_rating" : float(row["min_rating"]),
        "member_since" : "2022"
    })
user_col.insert_many(user_docs)
print(f"Insearted {len(user_docs)} users into database")
#rating and time transformation
rating_with_titles = ratings_df.merge(movies_df[["movieId", "title"]],on ="movieId", how = "left")
rating_with_titles["date"] = pd.to_datetime(rating_with_titles["timestamp"], unit="s").dt.strftime("%Y-%m-%d")
rating_docs = []
for _, row in rating_with_titles.iterrows():
    rating_docs.append({
        "user_id" : int(row["userId"]),
        "movie_id" : int(row["movieId"]),
        "movie_title" : str(row["title"]).strip(),
        "rating"  : float(row["rating"]),
        "date" : row["date"]
    })
#insert data into batch(chunking)
batch_size = 10000
for i in range(0,len(rating_docs),batch_size):
    batch = rating_docs[i:i+batch_size]
    ratings_col.insert_many(batch)
    print(f"Inserted batch {i//batch_size + 1} with {len(batch)}ratings into database")
#varify the data
print("\n"+"="*40)
print("database summary:")
print("="*40)
print(f"total movies:{movies_col.count_documents({})}")
print(f"total users: {user_col.count_documents({})}")
print(f"total ratings: {ratings_col.count_documents({})}")
print("Movies dataset loaded successfully")
sample = movies_col.find_one({},{"_id":0})
print(sample)
sample_user = user_col.find_one({},{"_id":0})
print(sample_user)
sample_rating = ratings_col.find_one({},{"_id":0})
print(sample_rating)


                                      
