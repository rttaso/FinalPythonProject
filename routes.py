from os import path

from werkzeug.utils import secure_filename
from form import RateFilm, SignInForm, SignUpForm, FavFilm, CommentForm
from flask import render_template, request, redirect, flash, url_for
from extensions import app
from models import FilmList, db, User, Film, Comment
from flask_login import login_user, logout_user, login_required, current_user


films = [
    {"id": 1, "name": "Pulp Fiction", "year": 1994, "rate": 5, "image": "/static/pulp_fiction.jpg"},
    {"id": 2,"name": "Black Swan", "year": 2010, "rate": 5, "image": "/static/MV5BNzY2NzI4OTE5MF5BMl5BanBnXkFtZTcwMjMyNDY4Mw@@._V1_.jpg"},
    {"id": 3,"name": "A Clockwork Orange", "year": 1971, "rate": 4, "image": "/static/orange.jpg"},
]


@app.route("/")
def home():
    return render_template("index.html", films=films)


@app.route("/films")
def list_films():
    films_list = FilmList.query.all()
    return render_template("films.html", films=films_list)


@app.route("/404")
def error():
    return render_template("404.html")


@app.route("/rate", methods=['GET', 'POST'])
@login_required
def rate_film():
    form = RateFilm()

    if form.validate_on_submit():
        file = form.image.data
        filename = file.filename
        file.save((path.join(app.root_path, 'static', filename)))
        new_film = FilmList(
            name=form.name.data,
            year=form.year.data,
            rate=form.rate.data,
            image_filename=filename
        )

        db.session.add(new_film)
        db.session.commit()

    return render_template("rate.html", form=form)


@app.route("/view_film/<int:film_id>")
def view_film(film_id):
    form = CommentForm()
    film = FilmList.query.get(film_id)

    if not film:
        return redirect("/404")

    return render_template("view_film.html", film=film, form=form)


@app.route("/edit_film/<int:film_id>", methods=['GET', 'POST'])
@login_required
def edit_film(film_id):
    if current_user.role != "admin":
        return redirect("/")
    film = FilmList.query.get(film_id)
    if not film:
        return render_template("404.html")
    form = RateFilm(name=film.name, year=film.year, rate=film.rate)
    if form.validate_on_submit():
        film.name = form.name.data
        film.year = form.year.data
        film.rate = form.rate.data

        db.session.commit()

    return render_template("rate.html", form=form)


@app.route('/delete_film/<int:film_id>')
@login_required
def delete_film(film_id):
    if current_user.role != "admin":
        return redirect("/")
    film = FilmList.query.get(film_id)
    if not film:
        return render_template("404.html")
    db.session.delete(film)
    db.session.commit()
    flash("ფილმი წაიშალა")
    return redirect("/films")


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
        films = FilmList.query.filter(FilmList.name.ilike(f"%{search_query}%")).all()
    else:
        films = []

    return render_template("index.html", films=films)


@app.route('/signup', methods=['GET', 'POST'])
def register():
    form = SignUpForm()

    if form.validate_on_submit():
        existing_user = User.query.filter(User.username == form.username.data).first()
        if existing_user:
            flash("სახელი დაკავებულია.")
            return redirect("/signup")
        else:
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
        return redirect("/")

    return render_template("signup.html", form=form)


@app.route('/sign', methods=['GET', 'POST'])
def signin():
    form = SignInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(form.password.data):
            login_user(user)
        else:
            flash('არასწორი სახელი ან პაროლი.', 'danger')

    return render_template('sign.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = FavFilm()
    if form.validate_on_submit():
        film_instance = Film(filmName=form.filmName.data)

        db.session.add(film_instance)
        db.session.commit()
        return redirect("/")

    return render_template("profile.html", form=form)


@app.route('/add_comment/<int:film_id>', methods=['POST'])
@login_required
def add_comment(film_id):
    film = FilmList.query.get_or_404(film_id)
    form = CommentForm()

    if form.validate_on_submit():
        content = form.content.data
        comment = Comment(content=content, user=current_user, film=film)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('view_film', film_id=film.id))

    return render_template('view_film.html', film=film, form=form)
