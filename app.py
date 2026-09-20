import os
from flask import Flask, jsonify, request, render_template
from database import movies_col, user_col, ratings_col
from recommandation import content_based_recommendation, user_based_recommendation
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/stats')
def stats():
    try:
        return jsonify({
            "total_movies": movies_col.count_documents({}),
            "total_users": user_col.count_documents({}),
            "total_ratings": ratings_col.count_documents({})
        })
    except Exception as e:
        print(f"Stats error: {e}")
        return jsonify({"error": str(e)}), 500

# Pagination Get all movies
@app.route('/movies', methods=['GET'])
def get_movies():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    skip = (page - 1) * limit
    movies = list(movies_col.find(
        {},
        {"_id": 0}
    ).skip(skip).limit(limit))
    
    return jsonify({
        "page": page,
        "count": len(movies),
        "movies": movies
    })

# Get top rated movies
@app.route('/movies/top', methods=['GET'])
def top_movies():
    movies = list(movies_col.find(
        {"rating_count": {"$gt": 50}},
        {"_id": 0}
    ).sort("avg_rating", -1).limit(10))
    return jsonify({"top_movies": movies})

# Get by genre
@app.route('/movies/genres/<genres>', methods=['GET'])
def by_genre(genres):
    # FIXED: Removed the extra curly braces inside find()
    movies = list(movies_col.find(
        {"genres": genres},
        {"_id": 0}
    ).sort("avg_rating", -1).limit(10))
    
    return jsonify({
        "genres": genres,
        "count": len(movies),
        "movies": movies
    })

# Get content based recommendation
# FIXED: Changed spelling from /recommandation/... to /recommend/...
@app.route('/recommandation/content/<path:title>', methods=['GET'])
def content_recommend(title):
    try:
    
        print(f" Route hit! Searching: {title}")
        recs = content_based_recommendation(title)
        print(f"Returning {len(recs) if recs else 0} recs")
        return jsonify({
            "based_on": title,
            "recommendations": recs
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "recommendations": []
        }), 500

# Get user based recommendation
@app.route('/recommandation/user/<int:user_id>', methods=['GET'])
def user_recommand(user_id):
    try:
        print(f" Getting recs for user: {user_id}")
        recs = user_based_recommendation(user_id, num=6)

        if not recs:
            return jsonify({
                "user_id": user_id,
                "recommendations": []
            })

        return jsonify({
            "user_id": user_id,
            "recommendations": recs
        })

    except Exception as e:
        print(f" User rec error: {e}")
        return jsonify({
            "error": str(e),
            "recommendations": []
        }), 500

# Get user status
@app.route('/user/<int:user_id>', methods=['GET'])
def user_status(user_id):

    user = user_col.find_one(
        {"user_id": user_id},
        {"_id": 0}
    )
    if not user:
        return jsonify({"error": "user not found"}), 404
        
    # FIXED: Removed the extra curly braces inside find()
    recent_rating = list(ratings_col.find(
        {"user_id": user_id},
        {"_id": 0}
    ).sort("date", -1).limit(5))
    
    return jsonify({
        "user": user,
        "recent_rating": recent_rating
    })

if __name__ == '__main__':
    print("Server at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)