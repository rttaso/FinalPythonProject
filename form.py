from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, HiddenField, TextAreaField
from wtforms.fields import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.fields import FileField
from wtforms.validators import DataRequired, NumberRange, Length


class RateFilm(FlaskForm):
    name = StringField("სახელი", validators=[DataRequired()])
    year = IntegerField("გამოშვების წელი", validators=[DataRequired()])
    rate = IntegerField("შეფასება", validators=[DataRequired(), NumberRange(min=0, max=5)])
    image = FileField("ფოტო", validators=[DataRequired()])
    hidden_field = HiddenField()
    submit = SubmitField("დამატება")


class SignUpForm(FlaskForm):
    username = StringField('სახელი', validators=[DataRequired()])
    password = PasswordField('პაროლი', validators=[DataRequired(), Length(min=8, max=24)])
    hidden_field = HiddenField()
    submit = SubmitField('რეგისტრაცია')


class SignInForm(FlaskForm):
    username = StringField('სახელი', validators=[DataRequired()])
    password = PasswordField('პაროლი', validators=[DataRequired()])
    submit = SubmitField('შესვლა')


class FavFilm(FlaskForm):
    filmName = StringField('ფილმის სახელი', validators=[DataRequired()])
    submit = SubmitField('არჩევა')


class CommentForm(FlaskForm):
    content = TextAreaField('განხილვა', validators=[DataRequired()])
    submit = SubmitField('დაპოსტვა')



