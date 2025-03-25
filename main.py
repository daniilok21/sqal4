from flask import Flask, render_template, redirect, request, abort, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.jobs import Jobs
from data.users import User
from data.news import News
from forms.job import JobForm
from forms.user import RegisterForm, LoginForm
from forms.news import NewsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message="Пароли не совпадают")

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, message="Пользователь уже существует")

        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News(
            title=form.title.data,
            content=form.content.data,
            is_private=form.is_private.data,
            user=current_user
        )
        db_sess.add(news)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()

    if not news:
        abort(404)

    if form.validate_on_submit():
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        db_sess.commit()
        return redirect('/')
    elif request.method == 'GET':
        form.title.data = news.title
        form.content.data = news.content
        form.is_private.data = news.is_private
    return render_template('news.html', form=form)


@app.route('/news_delete/<int:id>')
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()

    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        try:
            leader = db_sess.get(User, int(form.team_leader.data))
            if not leader:
                raise ValueError("Руководитель не найден")
            job = Jobs(
                job=form.job.data,
                team_leader=int(form.team_leader.data),
                work_size=form.work_size.data,
                collaborators=form.collaborators.data,
                is_finished=form.is_finished.data
            )
            db_sess.add(job)
            db_sess.commit()
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
        db_sess.close()
    return render_template('add_job.html', form=form)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    try:
        jobs = db_sess.query(Jobs).join(User).all()
        return render_template("jobs.html", jobs=jobs)
    except Exception as e:
        print(e)
    db_sess.close()


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=5000, debug = True)