from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import Blueprint,render_template,current_app,session,url_for,\
    redirect,request,flash
from app.forms import PostForm
from flask_login import login_required,current_user
from app.models import Posts
from app.extensions import db

main = Blueprint("main",__name__)

@main.route("/",methods=['POST','GET'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        u = current_user._get_current_object()
        p = Posts(content=form.content.data,user=u)
        db.session.add(p)
        return redirect(url_for('main.index'))
        #读取所有发表的博客
        # posts = Posts.query.filter_by(rid=0).all()
    # 只保留发表的博客，然后按照时间倒序排列
    page = request.args.get('page', 1, type=int)
    # 只保留发表的博客，然后按照时间倒序排列
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=15,
                                                                                        error_out=False)
    posts = pagination.items
    return render_template("main/index.html",form=form,posts=posts,pagination=pagination)



