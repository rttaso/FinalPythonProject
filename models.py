from extensions import db, app, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def save(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)


    def __init__(self, username, password, role="guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class FilmList(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    year = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    image_filename = db.Column(db.String)

    comments = db.relationship('Comment', backref='film')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    film_id = db.Column(db.Integer, db.ForeignKey('film_list.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref='comments')


class Film(db.Model):
    filmName = db.Column(db.String, primary_key=True)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        admin_user = User(username="admin1", password="987654321", role="admin")
        admin_user2 = User(username="admin2", password="88888888", role="admin")
        pulp_fiction = FilmList(name="Pulp Fiction", year=1994, rate=5, image_filename="/static/pulp_fiction.jpg")
        black_swan = FilmList(name="Black Swan", year=2010, rate=5,
                              image_filename="/static/MV5BNzY2NzI4OTE5MF5BMl5BanBnXkFtZTcwMjMyNDY4Mw@@._V1_.jpg")
        mechanical = FilmList(name="A Clockwork Orange", year=1971, rate=4, image_filename="/static/orange.jpg")
        admin_user.create()
        admin_user2.create()
        pulp_fiction.create()
        black_swan.create()
        mechanical.create()
