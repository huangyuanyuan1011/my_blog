from flask import Blueprint, render_template, flash, redirect, url_for, current_app, session, request
from app.extensions import db, photos
from app.forms import Register_Form, Login_Form, Change_Password, Change_Email, UploadForm
from app.models import User
import os, random
from app.email import send_mail
from flask_login import login_user, login_required, logout_user, current_user
from PIL import Image

user = Blueprint("user", __name__)


@user.route("/register/", methods=["GET", "POST"])
def register():
    form = Register_Form()
    if form.validate_on_submit():
        # 根据表单数据，创建用户对象
        u = User(username=form.username.data, password=form.password.data,
                 email=form.email.data)
        # 将用户对象保存到数据库
        db.session.add(u)
        # 因为下面生成token需要使用id，此时还没有，因此需要手动提交
        db.session.commit()
        # 生成token
        token = u.generate_activate_token()
        # 发送用户账户的激活邮件
        send_mail(u.email, "注册账户激活", "email/activate", username=u.username, token=token)
        # 弹出flash消息提示用户
        flash("已注册成功，请点击邮件中的链接完成激活")
        # 跳转到首页/登录页面
        return redirect(url_for('main.index'))

    return render_template("user/register.html", form=form)


@user.route('/activate/<token>')
def activate(token):
    if User.check_activate_token(token):
        flash('账户已激活')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('user.register'))


@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u:
            flash('无效的用户名')
        elif not u.confirm:
            flash('账户尚未激活，请激活后再登录')
        elif u.verify_password(form.password.data):
            login_user(u, remember=form.remember.data)
            flash('登录成功')
            # 若get参数中有next则跳转到next位置，没有则跳转到首页
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('无效的密码')
    return render_template('user/login.html', form=form)


@user.route('/logout/')
def logout():
    logout_user()
    flash("你已退出登录！")
    return redirect(url_for('user.login'))


@user.route('/test/')
@login_required
def test():
    return '登陆后才可以访问！'


@user.route('/userinfo/')
@login_required
def userinfo():
    return render_template('user/userinfo.html')


@user.route('/change_password/', methods=["GET", "POST"])
@login_required
def change_password():
    form = Change_Password()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpassword.data):
            current_user.password = form.newpassword.data
            db.session.add(current_user)
            flash("密码修改成功,请重新登陆！")
            return redirect(url_for('user.login'))
        else:
            flash("原密码输入不正确，请重新输入！")
    return render_template('user/change_password.html', form=form)


@user.route("/change_email/", methods=["GET", "POST"])
@login_required
def change_email():
    form = Change_Email()
    u = current_user._get_current_object()
    if form.validate_on_submit():
        u.email = form.newemail.data
        db.session.add(u)
        flash("恭喜你邮箱修改成功！")
        return redirect(url_for('user.userinfo'))

    return render_template("user/change_email.html", form=form)


@user.route('/change_icon/', methods=["POST", "GET"])
@login_required
def change_icon():
    form = UploadForm()
    if form.validate_on_submit():
        # 获取文件后缀
        suffix = os.path.splitext(form.icon.data.filename)[1]
        filename = random_string() + suffix
        photos.save(form.icon.data, name=filename)
        # 生成缩略图
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
        img = Image.open(pathname)
        img.thumbnail((128, 150))
        img.save(pathname)
        # 删除原来的头像(不是默认的头像才删除)
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))
        # 保存修改至数据库
        current_user.icon = filename
        db.session.add(current_user)
        flash('头像已保存')
        return redirect(url_for('user.change_icon'))
    img_url = photos.url(current_user.icon)
    return render_template('user/change_icon.html', form=form, img_url=img_url)


def random_string(length=32):
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(base_str) for i in range(length))
