import os
from datetime import datetime

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import UserMixin, LoginManager, logout_user, current_user, login_user, login_required, login_manager
from flask_share import Share
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_openid import OpenID

basedir = os.path.abspath(os.path.dirname(__file__))
share = Share()
# app instance
app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "/login"
oid = OpenID(app, os.path.join(basedir, 'tmp'))
"""
LoginManager comes with
is_authenticated
is_active
is_anonymous
get_id()
"""


@login_manager.user_loader
def load_user(student_id):
    return Student.query.get(int(student_id))


@login_manager.user_loader
def load_user(teacher_id):
    return Teacher.query.get(int(teacher_id))


# db location
# app.config[" SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "myApp.db")
db_name = "myapp.db"
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///C:\Users\chris\PycharmProjects\myApp\appdb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'husdagavafvaafbafbfbaavvuavafvfdbbfafabboavbav'
SECRET_KEY = "Your_secret_string"
app.config['ASSIGNMENT_UPLOAD_FOLDER'] = os.path.join(basedir, 'static/assignment/')


# db tables
class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_student = db.Column(db.Boolean, default=True)
    username = db.Column(db.String(100), index=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=True)
    # questions_asked = db.relationship('Question', backref='author', lazy='dynamic')

    questions_asked = db.relationship(
        'Question',
        foreign_keys='Question.student_id',
        backref='student',
        lazy=True
    )

    def __repr__(student):
        return student.username


class Teacher(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_teacher = db.Column(db.Boolean, default=True)
    username = db.Column(db.String(100), index=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    answers_requested = db.relationship('Question', backref='teacher', lazy='dynamic')

    # answers_requested = db.relationship(
    #     'Question',
    #     foreign_keys='Question.teacher_id',
    #     backref='teacher',
    #     lazy=True
    # )

    def __repr__(teacher):
        return teacher.username


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __repr__(self):
        return self.question


class Account_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    change_email = db.Column(db.String(100), index=True, nullable=True)
    location = db.Column(db.String(100), index=True, nullable=True)
    # change_image = db.Column(db.String(350), index=True, nullable=True)
    contact = db.Column(db.Integer, index=True, nullable=True)
    guardians_contact = db.Column(db.Integer, index=True, nullable=True)


####CRUD
#####create

# @app.route('/add_work', methods=['GET', 'POST'])
# @login_required
# def add_assignment():
#     # check request method
#     if request.method == 'POST' and request.files:
#         # POST request(TEXT data)
#         user_id = request.form.get('user_id')
#         title = request.form.get('the_title')
#         category = request.form.get('category')
#         content = request.form.get('content')
#
#         user_assignment = Assignment(
#             user_id=current_user.id,
#             title=title,
#             category=category,
#             content=content
#         )
#         # add assignment in to db table(Assignment())
#         db.session.add(user_assignment)
#         db.session.commit()
#         flash("Assignment created successfully", "text text-success")
#         return redirect('/school_work')
#     else:
#         # GET request
#         return render_template("/add_work.html", title="school_me | Add assignment page")
#

# @app.route('/school_work')
# @login_required
# def assignment_detail():
#     user_assignments = Assignment.query.filter_by(user_id=current_user.id)
#     if user_assignments.count() <= 0:
#         # user has no assignments
#         auth_user = False
#         return render_template("add_work.html", title="school_me | {} school_me", auth_user=auth_user)
#     else:
#         # user has assignment(s)
#         auth_user = True
#         return render_template("school_work.html", title="school_me | {} school_me", auth_user=auth_user,
#                                found_assignment=user_assignments)
#
#
# # try:
# #     # get all assignmnts for the current user
# #     found_assignment = Assignment.query.filter_by(user_id=current_user.id)
# #     # check if the 1st assignent user id is the same as current_user   id
# #     # if found_assignment[0].user_id == current_user.id:
# #     auth_user = True
# #     flash("Assignment found", "text text-success")
# #     return render_template("school_work.html", title="school_me | {} school_me".format(found_assignment.title), auth_user=auth_user, found_assignment=found_assignment)
# # except:
# #     auth_user = False
# #     found_assignment = None
# #     return render_template("add_work.html", title="school_me | {} school_me",
# #                            auth_user=auth_user, found_assignment=found_assignment)
# #
# # return render_template("profile.html", title="school_me | {} school_me".format(found_assignment.title),
# #                        found_assignment=found_assignment)
#
#
# @app.route('/work_update/', methods=['GET', 'POST'])
# @login_required
# def assignment_update():
#     update_assignments = Assignment.query.filter_by(user_id=current_user.id)
#     if request.method == 'POST':
#         user_id = request.form.get('user_id')
#         title = request.form.get('the_title')
#         category = request.form.get('category')
#         content = request.form.get('content')
#
#         update_assignments.title = title
#         update_assignments.category = category
#         update_assignments.content = content
#
#         new_assignment = Assignment(
#             user_id=current_user.id,
#             title=title,
#             category=category,
#             content=content
#         )
#         # update assignment in to db table(Assignment())
#         db.session.add(new_assignment)
#         db.session.commit()
#         auth_user = True
#         flash("Assignment updated successfully", "text text-success")
#         return redirect('/work_update')
#
#     else:
#         # user has no assignments
#         auth_user = False
#         return render_template("add_work.html", title="school_me | {} school_me", auth_user=auth_user)


# @app.route('/work_delete/<int:assignment_id>')
# @login_required
# def assignment_delete(assignment_id):
#     found_assignments = Assignment.query.get(assignment_id)
#     if found_assignments.user_id == current_user.id:
#         db.session.delete(found_assignments)
#         db.session.commit()
#         flash('deleted successfully')
#         return redirect('/work_details/')
#     else:
#         return redirect('/school_work')


####user auth routes

@app.route('/')
def index():
    return render_template("index.html", title="School_me")


@app.route('/sign_up', methods=['GET', 'POST'])
def signup_user():
    if request.method == 'GET':
        return render_template("sign_up.html", title="Signup page")
    else:

        username = request.form['user_name']
        email = request.form['user_email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        user = Student or Teacher.query.filter_by(email=email).first()
        if user:  # if a user is found,  redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect('/sign_up')
        elif user is not None:
            return render_template("sign_up.html", title="Signup page", message="{} continue".format(email))
        elif password1 != password2:
            return render_template("sign_up.html", title="Signup page", message="password don't match")
        else:  # hash password
            password = generate_password_hash(password1)
            # create instance of new user
            new_user = User(
                username=username,
                email=email,
                password=password,
                teacher=True,
                student=False
            )

            # add user into db
            db.session.add(new_user)
            # save user into db
            db.session.commit()

            return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", title="School_me | login page", message="Welcome to School_ME")
    else:
        # 1. grab data from form
        email = request.form['user_email']
        password = request.form['password1']
        remember = True if request.form.get('remember') else False

        user = Student or Teacher.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return redirect("/account")
        else:
            # A user with provided credentials does not exist
            flash('No Such User, want to join us? sign up.')
            return render_template("login.html", title="School_me | Login page")


@app.route('/account', methods=['GET', 'POST'])
@login_required
def profile():
    questions = Question.query.filter(Question.answer is not None).all()

    context = {
        'questions': questions
    }
    return render_template("account.html", name=current_user.username)


@app.route('/account_details', methods=['GET', 'POST'])
@login_required
def edit_profile():
    return render_template("account_details.html")


@app.route('/logout')
@login_required
def homepage():
    logout_user()
    return render_template("index.html", title="school_me| Home Page")


@app.route("/ask", methods=['GET', 'POST'])
@login_required
def ask():
    if request.method == 'POST':
        question = request.form['question']
        teacher = request.form['user_name']
        student = request.form['user_name']

        question = Question(
            question=question,
            teacher_id=teacher,
            student_id=student
        )

        db.session.add(question)
        db.session.commit()

        return redirect('index.html')

    teacher = Teacher.query.filter_by(teacher=True).all()

    context = {
        'teacher': teacher
    }
    return render_template("ask.html", title="school_me", **context)


@app.route('/answer/<int:question_id>', methods=['GET', 'POST'])
@login_required
def answer(question_id):
    if not current_user.teacher:
        return render_template('index.html', message="Oops! looks like you ain't a Teacher")

    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        question.answer = request.form['answer']
        db.session.commit()

        return redirect(url_for('"unanswered.html"'))

    context = {
        'question': question
    }

    return render_template("answer.html", title="school_me", **context)


@app.route('/question/<int:question_id>')
def question(question_id):
    question = Question.query.get_or_404(question_id)
    context = {
        'question': question
    }

    return render_template("question.html", title="school_me", **context)


@app.route("/unanswered")
@login_required
def unanswered():
    if not current_user.teacher:
        return redirect('/index.html')
    unanswered_questions = Question.query \
        .filter_by(teacher_id=current_user.id) \
        .filter(Question.answer is None) \
        .all()

    context = {
        'unanswered_questions': unanswered_questions
    }

    return render_template("unanswered.html", title="school_me", **context)


@app.route('/users')
@login_required
def users():
    if not current_user.admin:
        return redirect('index.html')

    users = Student or Teacher.query.filter_by(admin=False).all()

    context = {
        'users': users
    }

    return render_template("unanswered.html", title="school_me", **context)


@app.route('/promote/<int:teacher_id>')
@login_required
def promote(teacher_id):
    if not current_user.admin:
        return redirect(url_for("index.html"))

    user = Teacher.query.get_or_404(teacher_id)

    user.teacher = True
    db.session.commit()

    return render_template("users.html", title="school_me")


@app.errorhandler(404)
def page_not_found(e):
    return "page not found"


@app.errorhandler(500)
def internal_error(e):
    return "internal error"


if __name__ == "__main__":
    app.run(debug=True)
