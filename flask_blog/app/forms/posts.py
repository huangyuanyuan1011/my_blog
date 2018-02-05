from flask_wtf import FlaskForm
from wtforms  import TextAreaField,SubmitField
from wtforms.validators import Length

class PostForm(FlaskForm):
    content = TextAreaField("新的一天，记录新的状态......",render_kw={"placeholder":"这一刻的想法..."},
                            validators=[Length(6,500,message="输入的字段限制在6--500字以内")])
    submit = SubmitField('发表')

class CommentForm(FlaskForm):
    content = TextAreaField("",render_kw={"placeholder":"留下你的评论...."},validators=[Length(3,500,
                message="输入的字段限制在3--500个字符之间")])
    submit = SubmitField("提交评论")