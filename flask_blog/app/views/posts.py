from flask import Blueprint,jsonify,flash,session,request,redirect,render_template,url_for
from flask_login import current_user,login_required
from app.forms.posts import CommentForm
from app.models import User,Posts
from app.extensions import db



posts = Blueprint('posts',__name__)


@posts.route('/collect/<int:pid>')
def collect(pid):
    #判断是否收藏
    if current_user.is_favorite(pid):
        #取消收藏
        current_user.del_favorite(pid)
    else:
        #添加收藏
        current_user.add_favorite(pid)
    return jsonify({'result':'ok'})

@posts.route('/comment/',methods=["POST","GET"])
@login_required
def comment():
    form = CommentForm()
    #获取get参数中的content的ID值
    content_id = request.args.get('id',type=int)
    if form.validate_on_submit():
        # 获取参当前用户的id
        uid = current_user._get_current_object()
        p = Posts(rid=content_id,content = form.content.data,user = uid)
        db.session.add(p)
        flash("评论成功")
        return redirect(url_for('posts.comment',id=content_id))
    p = Posts.query.get(content_id)
    comment = Posts.query.filter_by(rid =content_id)
    return render_template('posts/comment.html',form=form,p=p,comment=comment)


@posts.route('/mine_publish/')
@login_required
def mine_publish():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.posts.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=5,error_out=False)
    comments = pagination.items
    return render_template("posts/mine_publish.html",comments=comments,pagination=pagination)


@posts.route('/mine_collect/')
def mine_collect():
    page =request.args.get('page',1,type=int)
    pagination = current_user.favorites.order_by(Posts.timestamp.desc()).paginate(page, per_page=5,error_out=False)
    comments = pagination.items
    return render_template("posts/mine_collect.html",pagination=pagination,comments=comments)

@posts.route('/comment_my/')
def comment_my():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.filter_by(uid=current_user.id)
    comment = []
    for post in posts:
        comment_me = Posts.query.filter_by(rid=post.id)
        for p in comment_me:
            comment.append(p)
    comment.reverse()

    return render_template("posts/comment_my.html", comments=comment)

