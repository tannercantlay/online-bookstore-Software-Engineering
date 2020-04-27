from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, AnyOf, Regexp, Optional
from app.models import User, Book, Promotion, Order, ListItem
from flask_wtf.file import FileRequired

class ConfirmationForm(FlaskForm):
    code = IntegerField('Confirmation Code')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    address = StringField('Address', validators=[Optional()])
    card_num=IntegerField('Credit Card Number', validators=[Optional()])
    card_exp = StringField('Expiration Date', validators=[Optional(),Regexp("\d{2}\/\d{4}")])
    subscribed = BooleanField('Subscribe to emails')
    submit = SubmitField('Register')
    cardtype = SelectField(u'Card Type', choices = [('c',"Credit"), ('d',"Debit")], validators = [Optional()])

    def validate_card_num(self, card_num):
        if not len(str(card_num.data))==16:
            raise ValidationError('Credit card number should be 16 digits long')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class UserInfo(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email')
    oldPassword = PasswordField('Old Password')
    address = StringField('Address')
    cardtype = SelectField(u'Card Type', choices = [('c',"Credit"), ('d',"Debit")], validators = [Optional()])
    card_num=IntegerField('Credit Card Number',validators=[Optional()])
    card_exp = StringField('Expiration Date', validators=[Regexp("\d{2}\/\d{4}"),Optional()])
    submit = SubmitField('Register')
    newPassword = PasswordField('New Password')
    newPassword2 = PasswordField('Repeat New Password', validators=[EqualTo('newPassword')])
    subscribed = BooleanField('Subscribe to emails')

    def validate_card_num(self, card_num):
        if not len(str(card_num.data))==16:
            raise ValidationError('Credit card number should be 16 digits long')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ForgotPassForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class BookInfo(FlaskForm):
    isbn = StringField('ISBN', validators = [DataRequired()])
    title = StringField('Title', validators = [DataRequired()])
    edition = StringField('Edition', validators = [DataRequired()])
    author = StringField('Author', validators = [DataRequired()])
    genre = StringField('Genre', validators = [DataRequired()])
    book_cover = FileField('Book Cover', validators = [FileRequired()])
    publisher = StringField('Publisher',validators = [DataRequired()])
    year_pub = StringField('Publication Year',validators = [DataRequired()])
    num_stock = StringField('Quantity',validators = [DataRequired()])
    buying_price = StringField('Buying Price',validators = [DataRequired()])
    selling_price = StringField('Selling Price', validators = [DataRequired()])
    submit = SubmitField('submit')

class EditBookInfo(FlaskForm):
    isbn = StringField('ISBN', validators = [DataRequired()])
    title = StringField('Title', validators = [DataRequired()])
    edition = StringField('Edition', validators = [DataRequired()])
    author = StringField('Author', validators = [DataRequired()])
    genre = StringField('Genre', validators = [DataRequired()])
    book_cover = FileField('Book Cover')
    publisher = StringField('Publisher',validators = [DataRequired()])
    year_pub = StringField('Publication Year',validators = [DataRequired()])
    num_stock = StringField('Quantity',validators = [DataRequired()])
    buying_price = StringField('Buying Price',validators = [DataRequired()])
    selling_price = StringField('Selling Price', validators = [DataRequired()])
    submit = SubmitField('submit')

class Checkout(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    cardtype = SelectField(u'Card Type', choices = [('c',"Credit"), ('d',"Debit")], validators = [DataRequired()])
    card_num=IntegerField('Credit Card Number', validators=[DataRequired()])
    card_exp = StringField('Expiration Date', validators=[Regexp("\d{2}\/\d{4}"),DataRequired()])
    card_cvv=IntegerField('CVV', validators=[DataRequired()])
    submit = SubmitField('submit')

class CheckoutOptional(FlaskForm):
    address = StringField('Address', validators=[Optional()])
    cardtype = SelectField(u'Card Type', choices = [('c',"Credit"), ('d',"Debit")], validators = [Optional()])
    card_num=IntegerField('Credit Card Number', validators=[Optional()])
    card_exp = StringField('Expiration Date', validators=[Regexp("\d{2}\/\d{4}"),Optional()])
    card_cvv=IntegerField('CVV', validators=[DataRequired()])
    submit = SubmitField('submit')


