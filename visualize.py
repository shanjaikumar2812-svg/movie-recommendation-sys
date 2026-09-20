from database import movies_col, user_col, ratings_col
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#fetch data from database
movies = list(movies_col.find(
    {"rating_count": {"$gt":20}},
    {"_id":0}
))
df = pd.DataFrame(movies)
# top 10 movies by rating
top_df = df.sort_values('avg_rating', ascending=False).head(10)
fig1 = px.bar (
    top_df,
    x='title', y='avg_rating',
    title=' Top 10 movies(min 20 rating)',
    color='avg_rating',
    color_continuous_scale='Blues',
    text='avg_rating'
)
fig1.update_traces(texttemplate='%{text:.2f}',textposition='outside')
fig1.update_layout(xaxis_tickangle=-45)
fig1.show()
#genre distribution
genre_df= df.explode('genres')
genre_count = genre_df.groupby('genres').size().reset_index(name='count')
genre_count = genre_count.sort_values('count',ascending=False).head(15)
fig2 = px.pie(
    genre_count,
    values = 'count',
    names = 'genres',
    title = 'genre distribution',
    hole = 0.4
)
fig2.show()
#rating distribution
rating_data = list(ratings_col.find(
    {},
    {"_id":0, "rating":1}
).limit(10000))
rating_df = pd.DataFrame(rating_data)
fig3 = px.histogram(
    rating_df,
    x = 'rating',
    title = "rating distribution",
    nbins =10,
    color_discrete_sequence=['#2563eb']
)
fig3.show()
#most rated movies
popular_df = df.sort_values('rating_count',ascending=False).head(10)
fig4 = px.bar(
    popular_df,
    x='title',y='rating_count',
    title="Most rated movies",
    color = 'rating_count',
    color_continuous_scale = 'Reds'
)
fig4.update_layout(xaxis_tickangle=-45)
fig4.show()
# user activity
user_data = list(user_col.find(
    {},
    {"_id":0,"total_ratings":1}
))
user_df = pd.DataFrame(user_data)
fig5 = px.histogram(
    user_df,
    x='total_ratings',
    title="user activity",
    nbins= 10,
    color_discrete_sequence=['#7c3aed']
)
fig5.show()
print("The visualizing chart has been completed"
      )

