from urllib.parse import urlsplit
from flask import redirect, url_for, flash, render_template, request, session
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models.Users import Users
from forms.user_form import RegistrationForm, LoginForm, ChangePasswordForm, EditProfileForm


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        client = Users(
            username=form.username.data,
            phone=form.phone.data,
            email=form.email.data
        )
        client.set_password(form.password.data)
        db.session.add(client)
        db.session.commit()
        flash("Ви успішно зареєстровані!", "success")
        return redirect(url_for('index'))
        # flash('Не всі поля заповені вірно.', 'danger')
    return render_template('auth/registration.html', title="Реєстрація", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(Users).filter(Users.phone == form.phone.data).first() or \
               db.session.query(Users).filter(Users.email == form.phone.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        flash('Невірні дані. Будь-ласка, спробуйте ще раз.', 'danger')
        return redirect(url_for('login'))
    return render_template('auth/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    logout_user()
    flash('Ви успішно вийшли.', 'success')
    return redirect(url_for('login'))


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Пароль успішно змінено!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Невірний поточний пароль', 'danger')
    return render_template('auth/change_password.html', title='Зміна паролю', form=form)


@app.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template('auth/profile.html', user=user)


# P2
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Профіль оновлено!', 'success')
        return redirect(url_for('profile'))
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.phone.data = current_user.phone
    return render_template('auth/edit_profile.html', title='Редагування профілю', form=form)
