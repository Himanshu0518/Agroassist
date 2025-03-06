from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,FloatField, StringField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

class SignupForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=2, max=10)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(4, 20)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=2, max=10)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(8, 20)]
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class TransactionForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    transaction_type = SelectField(
        'Type',
        choices=[('earning', 'Earning'), ('expense', 'Expense')],
        validators=[DataRequired()]
    )
    description = StringField('Description', validators=[Optional()])
    date = DateField('Date', validators=[DataRequired()])
    category = StringField('Category', validators=[Optional()])
    submit = SubmitField('Add Transaction')
