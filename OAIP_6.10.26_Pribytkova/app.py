from flask import Flask, render_template, redirect, session
import random

app = Flask(__name__)

app.secret_key = "super-secret-key"



movies = [
    {
        "id": 1,
        "title": "Интерстеллар",
        "year": 2014, 
        "genre": "научно-фантастический фильм",
        "rating": 8.7
    },
    {
        "id": 2,
        "title": "Матрица",
        "year": 1999,
        "genre": "научная фантастика, киберпанк, боевик.",
        "rating": 8.7
    },
    {
        "id": 3,
        "title": "Шрек",
        "year": 2001,
        "genre": "фэнтези, комедия, приключения, семейный.",
        "rating": 8.2
    },
    {
        "id": 4,
        "title": "Джентльмены",
        "year": 2019,
        "genre": "криминал, комедия, боевик",
        "rating": 8.7
    }
]


@app.route("/")
def index():

    favorites = session.get("favorites", [])

    return render_template(
        "index.html",
        movies=movies,
        favorites_count=len(favorites),
        favorites=favorites
    )



@app.route("/add/<int:movie_id>")
def add_favorite(movie_id):

    if "favorites" not in session:
        session["favorites"] = []

    favorites = session["favorites"]

    if movie_id not in favorites:
        favorites.append(movie_id)

    session["favorites"] = favorites
    return redirect("/")



@app.route("/favorites")
def favorites():

    favorite_ids = session.get("favorites", [])

    favorite_movies = []

    for movie in movies:
        if movie["id"] in favorite_ids:
            favorite_movies.append(movie)

    return render_template(
        "favorites.html",
        movies=favorite_movies
    )



@app.route("/remove/<int:movie_id>")
def remove_favorite(movie_id):

    favorites = session.get("favorites", [])

    if movie_id in favorites:
        favorites.remove(movie_id)

    session["favorites"] = favorites

    return redirect("/favorites")


@app.route("/clear")
def clear_favorites():

    session["favorites"] = []

    return redirect("/favorites")

@app.route("/random")
def movie_random():
    movie = random.choice(movies)
    return render_template("random.html", movie = movie)



if __name__ == "__main__":
    app.run(debug=True)
