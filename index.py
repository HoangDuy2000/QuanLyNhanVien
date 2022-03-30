from flask import Flask, render_template, session, request, redirect, url_for
from QuanLyNhaSach import app, login
import utils
from QuanLyNhaSach.admin import *
from flask_login import login_user, login_required
import cloudinary.uploader


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route("/")
def home():
    prods = utils.load_products()
    cates = utils.load_categories()

    return render_template('index.html',
                           product=prods, categories=cates)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/login', methods=['get', 'post'])
def login_post():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            user = utils.check_login(username=username, password=password)
            err_msg = 'Sai Tên Tài Khoản Hoặc Mật Khẩu!!!'
        except Exception as ex:
            err_msg = 'Hệ Thống Đang Bị Lỗi: ' + str(ex)

        if user:
            login_user(user=user)
            if utils.check_role(user):
                return redirect(url_for('home'))
            else:
                return redirect('/admin')

    return render_template('login.html', err_msg=err_msg)


@app.route('/register', methods=['get', 'post'])
def register_post():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('inputName')
        username = request.form.get('inputUser')
        email = request.form.get('email')
        password1 = request.form.get('password')
        password2 = request.form.get('confirmPassword')
        avatar = request.files.get('avatar')
        avatar_path=None
        try:
            if User.query.filter_by(name=name).first():
                err_msg = 'Tên Tài Khoản Đã Được Sử Dụng!!!'
                return render_template('register.html', err_msg=err_msg)

            if not password1.strip().__eq__(password2.strip()):
                err_msg = 'Mật Khẩu Không Khớp!!!'
                return render_template('register.html', err_msg=err_msg)

            if User.query.filter_by(email=email).first():
                err_msg = 'Địa chỉ Email Đã Được Sử Dụng!!!'
                return render_template('register.html', err_msg=err_msg)

            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']

        except Exception as ex:
            err_msg = 'Hệ Thống Đang Bị Lỗi: ' + str(ex)

        utils.add_user(name=name, username=username, password=password1, email=email, avatar=avatar_path)
        return redirect(url_for('login_post'))

    return render_template('register.html', err_msg=err_msg)


if __name__ == "__main__":
    app.run(debug=True)