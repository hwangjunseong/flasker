from flask import Flask, render_template

app =Flask(__name__)

@app.route('/')
def index():
    first_name = "junseong"
    stuff = "This is <strong>Bold<strong>"
    favorite_pizza = ["pepper", 'cheese' ,41]
    return render_template('index.html', first_name=first_name, stuff=stuff, favorite_pizza=favorite_pizza)
#titile trim striptags
@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    # return "<h1> Hello {}</h1>".format(name)
    return render_template('user.html', user_name=name)

#invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', 404)

#internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html', 500)
