from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5

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
Bootstrap5(app)

all_books = []


@app.route('/')
def home():
    return render_template('index.html', all_books = all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    form = MyForm()
    if form.validate_on_submit():
        new_item = {
            "title":form.title.data,
            "author": form.author.data,
            "rating": form.rating.data
        }
        all_books.append(new_item)
        print(all_books)
        return redirect(url_for('add'))
    return render_template('add.html', form= form)



if __name__ == "__main__":
    app.run(debug=True)

