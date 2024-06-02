from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm as so
import sqlalchemy as sa

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


class MyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    rating = StringField('Rating', validators=[DataRequired()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-book-collection.db"

db = SQLAlchemy(app)


class Book(db.Model):
    title: so.Mapped[str] = so.mapped_column(sa.String(64), primary_key=True)
    author: so.Mapped[str] = so.mapped_column(sa.String(250), index=True)
    rating: so.Mapped[int] = so.mapped_column(index=True)


Bootstrap5(app)
with app.app_context():
    db.create_all()
all_books = []


@app.route('/')
def home():
    all_books = db.session.execute(
        db.select(Book).order_by(Book.title)).scalars()
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    form = MyForm()
    if form.validate_on_submit():

        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            rating=form.rating.data
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('add'))
    return render_template('add.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
