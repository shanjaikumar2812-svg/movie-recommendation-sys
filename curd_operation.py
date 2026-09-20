#retriving data from database
from database import movies_col, user_col, ratings_col
print("="*40)
print("all movies")
print("="*40)
#fetch the multiple data
all_movies = movies_col.find(
    {},{"_id":0, "movieId": 1, "title": 1, "genres" : 1, "avg_rating" :1, "year" : 1}
).limit(10)
for movies in all_movies:
    print(f"{movies["title"]} ({movies["year"]}) {movies["avg_rating"]}")
print("\n" + "="*40)
print("action movies only")
print("="*40)
#filter by genre
action = movies_col.find(
    {"genres": "Action"},{"_id": 0, "movieId": 1, "title": 1, "avg_rating": 1}
).limit(8)
for m in action:
    print(f"{m["title"]}{m["avg_rating"]}")
#top rated movies
print("\n" + "="*40)
print("top rated movies")
print("="*40)
top = movies_col.find(
    {"avg_rating": {"$gt":4.0},
     "rating_count": {"$gt": 50}},
     {"_id": 0, "title": 1, "avg_rating": 1,"rating_count": 1}
).sort("avg_rating", -1).limit(10)
for m in top:
    print(f"{m['title']} {m['avg_rating']} ({m['rating_count']} ratings)")
#update a movie
print("\n"+ "="*40)
print("updating a movie")
print("="*40)
movies_col.update_one(
     {"title": "Toy Story"},
     {"$set": {"avg_rating": 4.9}}
)
updated = movies_col.find_one({"title": "Toy Story"})
print(f"updated movie: {updated['title']}")
#create a new movie
print("\n"+"="*40)
print("creting a new movies")
print("="*40)
new_movie = {
    "movie_id":9999,
    "title": "leo",
    "genres": ["Action","Thriller","Drama"],
    "year": 2022,
    "avg_rating": 4.5,
    "rating_count":79
    
}
result = movies_col.insert_one(new_movie)
print(f"Insearted leo movie:{result.inserted_id}")
#top active users
print("\n"+"="*40)
print("top active users")
print("="*40)
top_user = user_col.find(
    {"_id":0,"user_id":1, "avg_rating_given":1}).sort("total_rating", -1).limit(10)
for u in top_user:
    print(f"user_id:{u["user_id"]}{u["total_ratings"]}ratings | Avg={u["avg_rating_given"]}]")
#resent ratings
print("\n"+"="*40)
print("resent ratings")
print("="*40)
resent = ratings_col.find(
    {},{"_id":0, "user_id":1, "movie_title":1, "rating":1,"date":1}
).sort("date", -1).limit(10)
for r in resent:
    print(f"{r["user_id"]} rated'{r["movie_title"]}'{r["rating"]}")
print("curd operations completed")