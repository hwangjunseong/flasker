from flask import Flask, render_template, flash, request, redirect, url_for
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
# from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy.sql import func
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
# from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from .forms import UserForm, PasswordForm, PostForm, LoginForm, SearchForm

# from sqlalchemy.dialects.mysql import pymysql
#create a flask instance
app =Flask(__name__)
#add database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wktong6877@localhost:3307/our_users_database'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:wktong6877@localhost/our_users'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#secret key
app.config['SECRET_KEY'] = "abcd"
#initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# db.init_app(app)
#혹은 콘솔에 flask db init치기

#flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
# 사용자가 로그인되지 않은 상태에서 접근을 시도할 때 리디렉션될 로그인 화면의 URL을 지정 -> /login
login_manager.login_view ="login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#create model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)#nullable=False -> 공백없음
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added= db.Column(db.DateTime,  default=func.now())
    # date_added= db.Column(db.DateTime, default=datetime.utcnow)
    #do some password stuff
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Posts', backref = 'poster')
    #post에서는 poster라는 이름을 사용해서 user객체에 접근할수있다 poster.id -> user.id와 동일

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    #password 일치하는지 확인

    #password 입력한거 가져와서 hash함수적용해서 비밀번호를 해시로 변환
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    #password 확인
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    #create a string
    def __repr__(self):
        return '<Name %r>' %self.name
    

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=func.now())
    slug = db.Column(db.String(255))
    #create foreign key to link users -> users의 id -> 한명의 유저가 여러가지 post 가지기 가능 
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    



#navbar에 있는 csrf토큰이 form 인자로 전달되지않아서 base.html에 인자로 전달해줌
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

#create search function
@app.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        #submit form으로 부터 데이터 받아옴
        post.searched = form.searched.data
        #query the database
        #content 내용 filter함
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template('search.html', form=form, searched = post.searched , posts = posts)



#add post page
@app.route('/add-post', methods=['POST', 'GET'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        #poster은 user의 id
        poster = current_user.id
        post = Posts(title = form.title.data, content = form.content.data, poster_id = poster,slug = form.slug.data)
        #양식 초기화
        form.title.data = ''
        form.content.data = ''
        # form.slug.data = ''
        form.author.data = ''
        #post data database에 넣기
        db.session.add(post)
        db.session.commit()
        flash('Blog Post Submitted Successfully')
    #redirect to the website
    return render_template('add_post.html',form = form)

 #show post
@app.route('/posts')
def posts():
    #데이터베이스로부터 모든 포스트 grab -> 날짜순 정렬된거 기준으로
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

#개인의 post id로 블로그 봄
@app.route("/posts/<int:id>")
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html", post=post)


#post편집
@app.route("/posts/edit/<int:id>", methods=['POST', 'GET'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        #update data base
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated!")
        #redirect(url_for 안에는 함수이름이 들어간다
        #`url_for`함수는 엔드포인트 함수명을 인자로 받는다. 따라서 이동하고자 하는 라우트의 함수 이름을 url_for() 내에 적어줘야한다. 
        return redirect(url_for('post', id=post.id))
        # return redirect(url_for('malu', id=post.id))
    if current_user.id == post.poster_id:
        form.title.data = post.title
        # form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html',form=form)
    else:
        flash("Your are not authorized to edit this post")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)


#post삭제
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    # poster id -> user의 id와 일치하는 id만 delete할수있다
    if id == post_to_delete.poster_id:

        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post deleted successfully")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)
        except:
            flash("Post deleted failed, try again ")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)
    else:
        flash("Your are not authorized to delete that post")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)





@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        #데이터 베이스에 똑같은 이메일이 있는지 확인한다 이메일은 고유해야한다
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            #hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, method='pbkdf2:sha256')
            #고유하다면 데이터배이스에 추가
            user = Users(name=form.name.data,username = form.username.data, email = form.email.data, password_hash = hashed_pw)
            db.session.add(user)
            db.session.commit()
         
        name = form.name.data
        #초기화
        form.name.data = ''
        form.username.data=''
        form.email.data = ''
        form.password_hash.data = ''
        flash("User added Successfully")
    our_users = Users.query.order_by(Users.date_added).all()
    return render_template('add_user.html', form=form, name = name, our_users = our_users)    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User updated successfully")
            return render_template('update.html', form=form, name_to_update=name_to_update)
        except:
            flash("User updated failed")
            return render_template('update.html', form=form, name_to_update=name_to_update)
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update, id = id)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully")
        our_users = Users.query.order_by(Users.date_added).all()
        return render_template('add_user.html', form=form, name = name, our_users = our_users)

    except:
        flash("User deleted failed")
        return render_template('add_user.html', form=form, name = name, our_users = our_users)



#url_for에 함수이름 전달
@app.route('/')
def index():
    
    return render_template('index.html')


# @app.route('/test_pw', methods=['GET', 'POST'])
# def test_pw():
#     email = None
#     password = None
#     pw_to_check = None
#     passed = None

#     #form객체생성
#     form = PasswordForm()
#     #validate form -> post요청과 form데이터가 제출된경우
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password_hash.data
#         #clear form
#         form.email.data = ''
#         form.password_hash.data = ''
#         # flash("Form Submitted Successfully")

#         #데이터베이스에 이메일 같은거 있는지 확인
#         pw_to_check = Users.query.filter_by(email=email).first()
#         #check hashed password
#         passed = check_password_hash(pw_to_check.password_hash, password)
#         #true나 false반환
#     #인자로 name과 form을 전달한다
#     return render_template('test_pw.html', email=email, password = password,  pw_to_check = pw_to_check, passed = passed, form=form)


#create login page
@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #username = form.username.data , first()-> 방금전에 submit버튼에다가 username적은거 가져옴
        user = Users.query.filter_by(username = form.username.data).first()
        #username은 unique해서 하나만 존재
        if user:
            #check the hash
            if check_password_hash(user.password_hash, form.password.data):
                #비밀번호와 데이터베이스에 있는 해쉬된 비밀번호가 일치
                #로그인한고 세션을 생성해준다
                login_user(user)
                flash("Login successful")
                #dashboard함수로 redirect
                return redirect(url_for('dashboard'))
            else:
                #form에 입력한 password와 database에 있는 비밀번호가 틀렸습니다
                flash("Wrong password- try again")
        else:
            #user가 없을경우
            flash("That User does not exist")

    return render_template('login.html',form =form)

#create logout page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    #login함수로 redierect
    return redirect(url_for('login'))
#create dashboard page
@app.route('/dashboard',methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User updated successfully")
            return render_template('dashboard.html', form=form, name_to_update=name_to_update)
        except:
            flash("User updated failed")
            return render_template('dashboard.html', form=form, name_to_update=name_to_update)
    else:
        return render_template('dashboard.html', form=form, name_to_update=name_to_update, id = id)
    return render_template('dashboard.html')


#invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500






if __name__ == '__main__':


    app.run(debug=True)
