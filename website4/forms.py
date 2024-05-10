from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError 
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
# from flask_wtf.file import FileField
#create form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("UserName", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash= PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("submit")


class CrawlPostForm(FlaskForm):
    title = StringField("Enter your Title", validators=[DataRequired()])
    submit = SubmitField("submit")

class PostForm(FlaskForm):
            #title content date_posted category url

    title = StringField("What is your Title", validators=[DataRequired()])
    content = StringField("What is your Content", validators=[DataRequired()], widget = TextArea())
    category = StringField("What is your Category", validators=[DataRequired()])
    submit = SubmitField("submit")

class LoginForm(FlaskForm):
    username=StringField("Username", validators=[DataRequired()])
    password=PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("submit")
 
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("submit")