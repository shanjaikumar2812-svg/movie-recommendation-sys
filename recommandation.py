from database import movies_col, user_col, ratings_col
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
#content based filtering(genres) 
def content_based_recommendation(movie_title, num=5):
    print(f"content based recommendation for:{movie_title}")
    try:
        movies = list(movies_col.find(
            {"rating_count": {"$gt": 5}},
            {"_id": 0}
        ))
        df = pd.DataFrame(movies)

        if df.empty:
            return []

        df['genre_str'] = df['genres'].apply(
            lambda x: ' '.join(x) if isinstance(x, list) else str(x)
        )

        tfidf = TfidfVectorizer(stop_words='english')
        matrix = tfidf.fit_transform(df['genre_str'])
        similarity = cosine_similarity(matrix, matrix)

        # Partial match
        matches = df[df['title'].str.contains(
            movie_title, case=False, na=False, regex=False
        )]

        if matches.empty:
            print(f"Movie not found: {movie_title}")
            return []

        idx = matches.index[0]
        scores = sorted(
            list(enumerate(similarity[idx])),
            key=lambda x: x[1],
            reverse=True
        )[1:num+1]

        recs = df.iloc[
            [i[0] for i in scores]
        ][['title', 'genres', 'avg_rating', 'rating_count']]

        # Always return list not DataFrame!
        return recs.to_dict('records')

    except Exception as e:
        print(f"Error: {e}")
        return []
   
#collabrative filltering(user based)
def user_based_recommendation(user_id, num=5):
    print(f"collabrative_filtering recommendation for user_id:{user_id}")
    #fetch the data
    ratings = list(ratings_col.find(
        {},
        {"_id":0, "user_id":1, "movie_title":1, "rating":1}
    ).limit(20000))
    df= pd.DataFrame(ratings)
    #building the user matrix
    matrix = df.pivot_table(
        index="user_id",
        columns="movie_title",
        values="rating"
    ).fillna(0)
    if user_id not in matrix.index:
        print("user not found")
        return
    #find similar users
    sim = cosine_similarity(matrix)
    sim_df = pd.DataFrame(sim, index=matrix.index, columns=matrix.index)
    similar_user = sim_df[user_id].sort_values(ascending=False)[1:6].index
    #already watched
    watched = set(df[df['user_id']==user_id]['movie_title'])
    #generating recommendation
    recommendations = set()
    for sim_user in similar_user:
        sim_movies = set(df[df['user_id']==sim_user]['movie_title'])
        new_movies = sim_movies - watched
        recommendations.update(list(new_movies)[:3])
        if len(recommendations) >= num:
            break
    #final output
    recs = list(recommendations)[:num]
    for r in recs:
        print(f"{r}")
        return recs
print("="*40)
print("content based recommendation")
print("="*40)
content_based_recommendation("Toy story")
print("="*40)
print("user based recommendation")
print("="*40)
user_based_recommendation(1)
