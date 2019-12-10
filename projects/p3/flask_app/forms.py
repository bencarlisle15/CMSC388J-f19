from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email

class PostForm(FlaskForm):
  name = StringField("Name",  [InputRequired("Please enter your name.")])
  email = StringField("Email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
  title = StringField("Title",  [InputRequired("Please enter a title.")])
  content = TextAreaField("Content",  [InputRequired("Please enter your content")])
  submit = SubmitField("Send")

class CommentForm(FlaskForm):
  name = StringField("Name",  [InputRequired("Please enter your name.")])
  content = TextAreaField("Content",  [InputRequired("Please enter your content")])
  submit = SubmitField("Send")
