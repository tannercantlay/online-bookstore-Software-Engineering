from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, index=True)
    last_name = db.Column(db.String(50), nullable=False, index=True)
    email = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(75), nullable=True)
    card_num = db.Column(db.String(128), nullable=True)
    subscribed = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    email_val = db.Column(db.Integer, nullable=True)
    admin = db.Column(db.Boolean, nullable=True)
    card_exp = db.Column(db.String(128), nullable=True)
    cardtype = db.Column(db.String(1), nullable=True)
    last_four = db.Column(db.String(4), nullable=True)


    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_card_num(self, card_num):
        self.card_num = generate_password_hash(str(card_num))

    def check_card_num(self, other_card_num):
        return check_password_hash(self.card_num, str(other_card_num))

    def set_card_exp(self, card_exp):
        self.card_exp = generate_password_hash(str(card_exp))

    def check_card_exp(self, other_card_exp):
        return check_password_hash(self.card_exp, str(other_card_exp))



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Book(db.Model):
    isbn = db.Column(db.Integer, primary_key=True, unique=True, index=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    edition = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    book_cover = db.Column(db.String(75), nullable=False)
    publisher = db.Column(db.String(50), nullable=False)
    year_pub = db.Column(db.Integer, index=True)
    buying_price = db.Column(db.Numeric(), nullable=False)
    selling_price = db.Column(db.Numeric(), nullable=False)
    num_stock = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Book {}>'.format(self.title)
    def get_buying_price(self):
        return round(self.buying_price,2)
    def get_selling_price(self):
        return round(self.selling_price,2)

class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    promo_code = db.Column(db.String(12), nullable=False)
    percentage = db.Column(db.Numeric(), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Promotion {}>'.format(self.promo_code)

class ListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    order_id = db.Column(db.Integer, nullable=False)
    book_item = db.Column(db.Integer, nullable=False)
    book_quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<ListItem {}>'.format(self.id)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    user_id = db.Column(db.Integer)
    status =db.Column(db.String(25), nullable=False)
    total = db.Column(db.Numeric(), nullable=False)
    discount_total = db.Column(db.Numeric(), nullable=True)
    promo_id = db.Column(db.Integer, nullable=True)
    shipping_info = db.Column(db.String(75), nullable=True)
    card_num = db.Column(db.String(128), nullable=True)
    card_exp = db.Column(db.String(128), nullable=True)
    cardtype = db.Column(db.String(1), nullable=True)
    last_four = db.Column(db.String(4), nullable=True)
    confirmation_num = db.Column(db.Integer, unique=True)
    order_date = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<Order {}>'.format(self.id)
    def get_total(self):
        return round(self.total,2)
    def get_discount_total(self):
        return round(self.discount_total,2)
    def set_card_num(self, card_num):
        self.card_num = generate_password_hash(str(card_num))
    def set_card_exp(self, card_exp):
        self.card_exp = generate_password_hash(str(card_exp))
