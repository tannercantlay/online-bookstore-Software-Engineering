import os
from flask import render_template, flash, redirect, request, url_for, session
from app import app, db, mail
from app.forms import LoginForm, RegistrationForm
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Book, Promotion, Order, ListItem
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_mail import Message
from random import randint
import random
import string
from datetime import date, datetime
from decimal import Decimal

@app.route('/')
@app.route('/index.html')
def index():
    #print(session.get('orderId'))
    return render_template('index.html',title='index')

@app.route('/browse.html',methods=['GET','POST'])
def browse():
    searchBy = request.args.get('searchBy')
    keyword = request.args.get('keyword')
    if searchBy and keyword:
        if searchBy == "Author":
             books = Book.query.filter_by(author=keyword)
        elif searchBy == "Genre":
             books = Book.query.filter_by(genre=keyword)
        else:
             books = Book.query.filter_by(title=keyword)
    else:
        books= Book.query.all()
    return render_template('browse.html',title='browse',books=books)


@app.route('/account_settings.html', methods=['GET', 'POST'])
@login_required
def account_settings():
    form=UserInfo()
    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.address.data = current_user.address
        form.subscribed.data = current_user.subscribed
        form.cardtype.data = current_user.cardtype

    elif form.validate_on_submit():
        pass_change=form.newPassword.data and form.newPassword2.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.address = form.address.data
        current_user.subscribed = form.subscribed.data
        current_user.cardtype = form.cardtype.data
        current_user.last_four = form.card_num.data%10000 if form.card_num.data else current_user.last_four
        if(form.card_num.data):
            current_user.set_card_num(form.card_num.data)
        if(form.card_exp.data):
            current_user.set_card_exp(form.card_exp.data)

        if pass_change:
            if current_user.check_password(form.oldPassword.data):
                current_user.set_password(form.newPassword.data)
            else:
                flash('Incorrect old password, password changes not made. All other changes made successfully.')
                return render_template('account_settings.html',title='settings', form=form)

        msg = Message("Account information changed!",
                  sender="Agroup7bookstore@gmail.com",
                  recipients=[current_user.email])
        msg.body = "A change has been made to the account associated with the email: {}".format(current_user.email)
        db.session.commit()
        mail.send(msg)
        flash('Account changes for {} have been made successfully'.format(current_user.email))
        return redirect('/index.html')
    return render_template('account_settings.html',title='settings', form=form,
        hasLast=current_user.last_four is not None,
        credit= False if (current_user.cardtype is None or current_user.cardtype=='d') else True)

@app.route('/forgotpassword.html', methods=['GET', 'POST'])
def forgot_pass():
    form=ForgotPassForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            myUser = User.query.filter_by(email=form.email.data).first()
            chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
            temp_password =''.join(random.choice(chars) for x in range(8))
            myUser.set_password(temp_password)
            msg = Message("Forgotten Password Request!",
                  sender="Agroup7bookstore@gmail.com",
                  recipients=[form.email.data])
            msg.body = "A request has been made to gain access to your account. Remember to change your password when you login next. To login, please use this temporary password: {}".format(temp_password)
            db.session.commit()
            mail.send(msg)
            flash('Instructions to access your account have been emailed to {}'.format(form.email.data))
        else:
            flash('Email not recognized in the system!')
    return render_template('forgotpassword.html',title='Forgot Password', form=form)

@app.route('/create_account.html', methods=['GET', 'POST'])
def create_account():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    print("DEBUG: Form valid", form.validate())


    if form.validate_on_submit():
        conf_code = randint(1000, 9999)
        user = User(first_name=form.first_name.data,
            last_name=form.last_name.data, admin=False,
            cardtype=form.cardtype.data, address=form.address.data,
            email=form.email.data, subscribed=form.subscribed.data,
            active=False, email_val = conf_code,
            last_four=form.card_num.data%10000 if form.card_num.data else None)
        if(form.card_num.data):
            user.set_card_num(form.card_num.data)
        if(form.card_exp.data):
            user.set_card_exp(form.card_exp.data)
        user.set_password(form.password.data)
        db.session.add(user)
        msg = Message("Thank you for registering!",
                  sender="Agroup7bookstore@gmail.com",
                  recipients=[form.email.data])
        msg.body = "Thank you for registering for an account with our online bookstore! Your code to verify and activate your account is: {}".format(conf_code)
        db.session.commit()
        mail.send(msg)
        if session.get('orderId'):
            order = Order.query.filter_by(id = session.get('orderId')).first()
            order.user_id = user.id
            db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('create_account.html',title='create_user', form=form)



@app.route('/register.html', methods=['GET', 'POST'])
def register():
    form=ConfirmationForm()
    if form.validate_on_submit():
        if current_user.email_val==form.code.data:
            current_user.email_val= -1
            current_user.active = True
            db.session.commit()
            flash('Account {} has been activated'.format(current_user.email))
            redirect('/regconfirmation.html')

    return render_template('register.html',title='Activate Account', form=form)

@app.route('/regconfirmation.html')
def register_conf():
    return render_template('regconfirmation.html',title='Account Activated')

@app.route('/booklist.html')
def book_page():
    return render_template('booklist.html',title='edit booklist', books=Book.query.all())

@app.route('/addbook.html',  methods=['GET', 'POST'])
def add_book():
    form = BookInfo()
    if form.validate_on_submit():
        f = form.book_cover.data
        filename = secure_filename(f.filename)
        file_path = os.path.join(app.root_path, 'static', filename)
        f.save(file_path)
        book = Book(isbn=form.isbn.data,
            title=form.title.data, edition=form.edition.data,
            author=form.author.data, genre=form.genre.data,
            book_cover=filename, publisher=form.publisher.data,
            year_pub=form.year_pub.data, num_stock = form.num_stock.data,
            buying_price=form.buying_price.data, selling_price=form.selling_price.data)
        db.session.add(book)
        db.session.commit()
        flash('Book Saved')
        return redirect('booklist.html')
    return render_template('addbook.html',title='add book', form=form)


@app.route('/book_edit:<string:id>',  methods=['GET', 'POST'])
def edit_book(id):
    form = EditBookInfo()
    book = Book.query.filter_by(isbn=id).first()
    if request.method == 'GET':
        form.isbn.data = book.isbn
        form.title.data = book.title
        form.edition.data = book.edition
        form.author.data = book.author
        form.genre.data = book.genre
        form.publisher.data = book.publisher
        form.year_pub.data = book.year_pub
        form.num_stock.data = book.num_stock
        form.buying_price.data = book.buying_price
        form.selling_price.data = book.selling_price

    elif form.validate_on_submit():
        book.isbn = form.isbn.data
        book.title = form.title.data
        book.edition = form.edition.data
        book.author = form.author.data
        book.genre = form.genre.data
        book.publisher = form.publisher.data
        book.year_pub = form.year_pub.data
        book.num_stock = form.num_stock.data
        book.buying_price = form.buying_price.data
        book.selling_price = form.selling_price.data

        if form.book_cover.data:
            path_to_delete = os.path.join(app.root_path, 'static/{}'.format(book.book_cover))
            f = form.book_cover.data
            filename = secure_filename(f.filename)
            file_path = os.path.join(app.root_path, 'static', filename)
            f.save(file_path)
            book.book_cover = filename
            os.system('rm {}'.format(path_to_delete))

        db.session.commit()
        flash('Book Changes Saved')
        return redirect('booklist.html')
    return render_template('book.html',title='edit book', form=form, book=book)

@app.route('/delete:<string:id>', methods=['GET', 'POST'])
def delete_book(id):
    book = Book.query.filter_by(isbn=id).first()
    path_to_delete = os.path.join(app.root_path, 'static/{}'.format(book.book_cover))
    os.system('rm {}'.format(path_to_delete))
    db.session.delete(book)
    db.session.commit()
    flash('Book Deleted')
    return redirect('booklist.html')

@app.route('/add_to_cart:<int:bookId>', methods=['GET', 'POST'])
def add_to_cart(bookId):
    quantity = int(request.args.get("quantity"))
    order=None
    if current_user.is_authenticated:
        user = current_user
        order=Order.query.filter_by(user_id=current_user.id, status="current").first()
        # if user has no cart, create one
        if not order:
            order = Order(user_id=current_user.id, status="current", total=0.0)
            db.session.add(order)
            db.session.flush()
    else:
        #if anon user has no cart, create one
        if not session.get('orderId'):
            order = Order(status="current", total=0.0)
            db.session.add(order)
            db.session.flush()
            #add order id to session
            session['orderId'] = order.id
    orderId=order.id if order else session['orderId']
    item=ListItem.query.filter_by(book_item=bookId,order_id=orderId).first()
    book=Book.query.filter_by(isbn=bookId).first()


    if item:
        quantity+=item.book_quantity
        if quantity>book.num_stock:
            flash("Could not add to cart as requested quantity exceeds stock.")
            return redirect('browse.html')
        item.book_quantity=quantity
    else:
        if quantity>book.num_stock:
            flash("Could not add to cart as requested quantity exceeds stock.")
            return redirect('browse.html')
        item = ListItem(book_item=bookId, book_quantity=quantity, order_id=orderId)
        db.session.add(item)
    db.session.commit()
    flash('Items added to cart')

    return redirect('cart.html')

@app.route('/remove_from_cart:<string:id>', methods=['GET', 'POST'])
def delete_item(id):
    item = ListItem.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()
    flash('Item removed from cart')
    return redirect('cart.html')

@app.route('/promotion.html')
def add_promotion():
    return render_template('promotion.html',title='add promotion')

@app.route('/promotionlist.html')
def promotion_list():
    return render_template('promotionlist.html',title='promotion list')
@app.route('/orderhistory.html')
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id, status="completed")
    #display_items = [(item, Book.query.filter_by(isbn=item.book_item).first()) for item in ListItem.query.filter_by(order_id=orderId)]
    #need for each order -> price, date, book and quantity
    display_items=[]
    for order in orders:
        books_and_quantities = []
        for item in ListItem.query.filter_by(order_id=order.id):
            books_and_quantities.append([Book.query.filter_by(isbn=item.book_item).first().title, item.book_quantity])
        display_items.append([order, books_and_quantities])
    return render_template('orderhistory.html',title='order history', display_items=display_items)

@app.route('/order.html')
def order_view():
    return render_template('order.html',title='order view')

@app.route('/update_quantity:<string:id>')
def update_quantity(id):
    quantity = int(request.args.get("quantity"))
    item = ListItem.query.filter_by(id=id).first()
    book_stock = Book.query.filter_by(isbn=item.book_item).first().num_stock
    if quantity > book_stock:
        quantity = book_stock
        flash("quantity requested is more than stock, quantity set to current stock")
    else:
        flash("quantity updated")
    item.book_quantity = quantity
    db.session.commit()
    return redirect('cart.html')

@app.route('/employee.html')
def edit_employee():
    return render_template('employee.html',title='edit employee')

@app.route('/addemployee.html')
def add_employee():
    return render_template('addemployee.html',title='add employee')

@app.route('/userlist.html')
def user_list():
    return render_template('userlist.html',title='user_list')

@app.route('/user.html')
def edit_user():
    return render_template('user.html',title='edit user')

@app.route('/employeelist.html')
def employee_list():
    return render_template('employeelist.html',title='Employee List')

@app.route('/register.html')
def register_account():
    return render_template('register.html',title='register')

@app.route('/cart.html', methods=['GET', 'POST'])
def cart_page():

    orderId=None
    if current_user.is_authenticated:
        if Order.query.filter_by(user_id=current_user.id, status="current").first():
            orderId = Order.query.filter_by(user_id=current_user.id, status="current").first().id
    elif session.get('orderId'):
        orderId = session.get('orderId')
    display_items = []
    changed = False
    for item in ListItem.query.filter_by(order_id=orderId):
        book = Book.query.filter_by(isbn=item.book_item).first()
        if item.book_quantity > book.num_stock:
            item.book_quantity = book.num_stock
            changed = True
        display_items.append([item, book])
    if changed:
        db.session.commit()
        flash("One or more items in your cart had quantity that exceeded stock and have been updated")
        return redirect('cart.html')
    order=Order.query.filter_by(id=orderId, status="current").first()
    if not order:
        flash("Please add items to your cart before viewing cart")
        return redirect('browse.html')

    promo=request.args.get('promo')
    if promo is None:
        if Promotion.query.filter_by(id=order.promo_id).first():
            promo = Promotion.query.filter_by(id=order.promo_id).first().promo_code
        #promo = Promotion.query.filter_by(id=order.promo_id).first().id if Promotion.query.filter_by(id=order.promo_id).first() is not None
    promotion=None if not promo else Promotion.query.filter_by(promo_code=promo).first()
    order.promo_id = promotion.id if promotion else None



    total=0
    for i, j in display_items:
        total+=i.book_quantity*j.get_selling_price()
    order.total=Decimal(round(total, 3))
    dt=datetime.combine(date.today(), datetime.min.time())
    valid_date=False if promotion is None else (dt > promotion.start_date and dt < promotion.end_date)

    if promo and valid_date:
        total = Decimal(round(total, 3)) #This one stays
        total*=1-promotion.percentage
    order.discount_total=Decimal(round(total, 3))
    total=order.get_discount_total()
    db.session.commit()
    form = Checkout()
    if current_user.is_authenticated:
        if current_user.card_num and current_user.card_exp and current_user.last_four:
            order.card_num = current_user.card_num
            order.card_exp = current_user.card_exp
            order.last_four = current_user.last_four
            order.cardtype = current_user.cardtype
            form = CheckoutOptional()

    if request.method == 'GET' and current_user.is_authenticated:
        form.address.data = current_user.address
    if request.method == 'POST':
        if form.validate_on_submit():
            order.shipping_info = form.address.data
            if form.card_num.data:
                order.set_card_num(form.card_num.data)
                order.last_four = form.card_num.data%10000
            if form.card_exp.data: order.set_card_exp(form.card_exp.data)
            if form.cardtype.data: order.cardtype = form.cardtype.data
            order.order_date = datetime.combine(date.today(), datetime.min.time())
            order.confirmation_num = ('%020d'%order.id)
            order.status = "completed"
            ordered_items =  [(item[1].title, item[0].book_quantity) for item in display_items]
            for title, quantity in ordered_items:
                book = Book.query.filter_by(title=title).first()
                book.num_stock -= quantity
            msg = Message("Order Confirmation for order: {}!".format(order.id),
                    sender="Agroup7bookstore@gmail.com",
                    recipients=[current_user.email])
            msg.body = 'Hello {},\nThank you for ordering from our store!\n Your order confirmation number is: {} \nItems ordered include: {} \nYour total is :${} \nYour order date: {} \nThese items will be shipping to: {} \n\n Thank you for your service and have a great day!'.format(current_user.first_name, order.confirmation_num, ordered_items, order.discount_total, order.order_date, order.shipping_info)
            db.session.commit()
            mail.send(msg)
            return redirect('orderconfirmation:{}'.format(order.id))
        else:
            if not form.card_cvv.data:
                flash("Must enter cvv in checkout process")
            elif not form.address.data:
                flash("Must enter address in checkout process")
            else:
                flash("Must enter valid payment information in checkout process")




    return render_template('cart.html',title='view cart', items=display_items, form=form,order=order,promo=(promo is not None and valid_date, promo))


@app.route('/orderconfirmation:<string:id>')
def order_confirmation(id):
    order = Order.query.filter_by(id=id).first()
    return render_template('orderconfirmation.html',title='Order Confirmation', order=order)



@app.route('/login.html', methods=['GET', 'POST'])
def login():
    #if current_user.is_authenticated:
    #    return redirect(url_for('index'))

    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        orderId=session.get('orderId')
        order = Order.query.filter_by(user_id=user.id, status='current').first()
        print("anonymous order id: {}".format(orderId))
        print("registerd order id: ", order.id)
        if not order and orderId:
            order = Order.query.filter_by(id = orderId).first()
            order.user_id = user.id
        elif order and orderId:
            for item in ListItem.query.filter_by(order_id=orderId).all():
                print("book quantity: ", item.book_quantity )
                oi=ListItem.query.filter_by(order_id=order.id,book_item=item.book_item).first()
                print("found item in cart that matches listItem:", oi)
                if oi:
                    oi.book_quantity+=item.book_quantity
                    oi.book_quantity=min(oi.book_quantity,Book.query.filter_by(isbn=oi.book_item).first().num_stock)
                    print("merged item with existing item in cart")
                    print("new book quanity in cart", oi.book_quantity)
                else:
                    item.order_id=order.id
                    print("added item to cart")
                db.session.flush()
        if orderId:
            for item in ListItem.query.filter_by(order_id=orderId):
                db.session.delete(item)
            for o in Order.query.filter_by(id=orderId):
                db.session.delete(o)
            session.pop('orderId')
        db.session.commit()
        return redirect(next_page)

    return render_template('login.html',title='login',form=form)



@app.route('/logout.html', methods=['GET','POST'])
def logout():
    flash('Successfully logged out user {}'.format(current_user.email))
    logout_user()
    return redirect('login.html')

@app.route('/admin.html', methods=['GET', 'POST'])
def adminlogin():
    form=LoginForm()
    if form.validate_on_submit():
        flash('Login requested for Admin {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/booklist.html')
    return render_template('admin.html',title='login',form=form)
