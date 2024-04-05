from flask import Flask, render_template, Blueprint

users = Blueprint('users', __name__)

@users.route('/index/1')
def index():
    first_name = "junseong"
    stuff = "This is <strong>Bold<strong>"
    favorite_pizza = ["pepper", 'cheese' ,41]
    return render_template('index.html', first_name=first_name, stuff=stuff, favorite_pizza=favorite_pizza)
#titile trim striptags
@users.route('/<name>', methods=['GET', 'POST'])
def user(name):
    # return "<h1> Hello {}</h1>".format(name)
    return render_template('user.html', user_name=name)
    # first_name = "junseong"
    # first_name = name

    # stuff = "This is <strong>Bold<strong>"
    # favorite_pizza = ["pepper", 'cheese']
    # return render_template('index.html', first_name=first_name, stuff=stuff, favorite_pizza=favorite_pizza)

#invalid URL
@users.errorhandler(404)
def page_not_found():
    return render_template('404.html')

#internal Server Error
@users.errorhandler(500)
def page_not_found():
    return render_template('500.html')
