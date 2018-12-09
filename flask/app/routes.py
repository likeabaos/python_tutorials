from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.models import User, Post


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now live!")
        return redirect(url_for("index"))

    page = request.args.get("page", 1, type=int)
    posts = current_user.followed_posts().paginate(page, 3, False)
    prev_url = url_for("index", page=posts.prev_num) if posts.has_prev else None
    next_url = url_for("index", page=posts.next_num) if posts.has_next else None

    return render_template(
        "index.j2",
        title="Home",
        form=form,
        posts=posts.items,
        prev_url=prev_url,
        next_url=next_url,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        _user = User.query.filter_by(username=form.username.data).first()
        if _user is None or not _user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))

        login_user(_user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")

        return redirect(next_page)

    return render_template("login.j2", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        _user = User(username=form.username.data, email=form.email.data)
        _user.set_password(form.password.data)
        db.session.add(_user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))

    return render_template("register.j2", title="Register", form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    _user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter_by(user_id=_user.id)
        .order_by(Post.timestamp.desc())
        .paginate(page, 3, False)
    )
    prev_url = (
        url_for("user", username=username, page=posts.prev_num)
        if posts.has_prev
        else None
    )
    next_url = (
        url_for("user", username=username, page=posts.next_num)
        if posts.has_next
        else None
    )
    return render_template(
        "user.j2", user=_user, posts=posts.items, prev_url=prev_url, next_url=next_url
    )


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.j2", title="Edit Profile", form=form)


@app.route("/follow/<username>")
def follow(username):
    _user = validate_user(username, "follow")
    current_user.follow(_user)
    db.session.commit()
    flash("You are following {}!".format(username))
    return redirect(url_for("user", username=username))


@app.route("/unfollow/<username>")
def unfollow(username):
    _user = validate_user(username, "unfollow")
    current_user.unfollow(_user)
    db.session.commit()
    flash("You are no longer following {}!".format(username))
    return redirect(url_for("user", username=username))


def validate_user(username, action):
    _user = User.query.filter_by(username=username).first()
    if _user is None:
        flash("User {} not found".format(username))
        return redirect(url_for("index"))
    if _user == current_user:
        flash("Cannot {} yourself".format(action))
        return redirect(url_for("user", username=username))
    return _user


@app.route("/explore")
@login_required
def explore():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 3, False)
    prev_url = url_for("explore", page=posts.prev_num) if posts.has_prev else None
    next_url = url_for("explore", page=posts.next_num) if posts.has_next else None

    return render_template(
        "index.j2",
        title="Explore",
        posts=posts.items,
        prev_url=prev_url,
        next_url=next_url,
    )
