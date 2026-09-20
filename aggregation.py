from database import movies_col, user_col, ratings_col
#genre analytics
print("\n"+"="*40)
print("Genre analytics")
print("="*40)
pipeline1 = [
    {"$unwind": "$genres"},
    {"$group":{
        "_id": "$genres",
        "avg_rating":{"$avg":"$avg_rating"},
        "total_movies": {"$sum":1},
        "total_ratings": {"$sum": "$rating_count"}
    }},
    {"$sort": {"avg_rating": -1}},
    {"$limit": 10}
]
result1 = movies_col.aggregate(pipeline1)
for r in result1:
    print(f"{r['_id']} : Avg Rating = {r['avg_rating']:.2f} | Movies= {r['total_movies']}")
#Finding best movies
print("\n"+"="*40)
print("Best movies")
print("="*40)
# Best movie each decade
pipeline2 = [
    {"$match": {
        "year": {
            "$ne": "Unknown",
            "$exists": True,
            "$nin": [None, "", "Unknown"]
        }
    }},
    {"$addFields": {
        "year_int": {
            "$convert": {
                "input": "$year",
                "to": "int",
                "onError": 0,
                "onNull": 0
            }
        }
    }},
    {"$match": {"year_int": {"$gt": 0}}},
    {"$addFields": {
        "decade": {
            "$multiply": [
                {"$floor": {"$divide": ["$year_int", 10]}},
                10
            ]
        }
    }},
    {"$sort": {"avg_rating": -1}},
    {"$group": {
        "_id": "$decade",
        "best_movies": {"$first": "$title"},
        "best_rating": {"$first": "$avg_rating"},
        "rating_count": {"$first": "$rating_count"}
    }},
    {"$sort": {"_id": -1}},
    {"$limit": 5}
]
result2 = movies_col.aggregate(pipeline2)
for r in result2:
    print(f"decade:{r['_id']}s:{r['best_movies']} {r['best_rating']:.2f}")
#Most rated movies
print("\n"+"="*40)
print("most rated movies")
print("="*40)
pipeline3=[
    {"$sort": {"rating_count": -1}},
    {"$limit":10},
    {"$project":
     {"_id":0,
     "title":1,
     "avg_rating":1,
     "rating_count":1}}
]
result3=movies_col.aggregate(pipeline3)
for r in result3:
    print(f"{r['title']} : {r['rating_count']} ratings {r['avg_rating']:.2f}")
#User behaviour analysis
print("\n"+"="*40)
print("User behaviour analysis")
print("="*40)
pipeline4 = [
    {"$group":{
        "_id": None,
        "avg_rating": {"$avg": "$ratings"},
        "max_rating": {"$max": "$ratings"},
        "min_rating": {"$min": "$ratings"},
        "total_users": {"$sum":1}
    }}
]
result4 = movies_col.aggregate(pipeline4)
for r in result4:
    print(f"Total Users: {r['total_users']}")
    print(f"Avg rating: {r['avg_rating']}")
    print(f"Max rating: {r['max_rating']}")
    print(f"Min rating: {r['min_rating']}")
#disrributing ratings
print("n"+"="*40)
print("Distributing ratings")
print("="*40)
pipeline5= [
    {"$group":{
        "_id": "$rating",
        "count": {"$sum":1}
    }},
    {
        "$sort":{"_id":1}
    }
]
result5 = movies_col.aggregate(pipeline5)
for r in result5:
    bar = "█"  * (r['count'] // 1000)
    print(f"Rating: {r['_id']}: {bar} ({r['count']})")
print("Aggregation completed:")