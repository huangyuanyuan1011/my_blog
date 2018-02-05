from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError
from app.models import User
from flask_wtf.file import FileField,FileAllowed,FileRequired
from app.extensions import photos
#用户注册表单
class Register_Form(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(4, 20, message='用户名只能在4~20个字符之间')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20, message='密码长度必须在6~20个字符之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码不一致')])
    email = StringField('邮箱', validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('立即注册')

# 自定义字段验证函数，验证username
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户已注册，请选用其它用户名')

# 自定义字段验证函数，验证username
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册，请选用其它邮箱')


class Login_Form(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(4, 20, message='用户名只能在4~20个字符之间')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20, message='密码长度必须在6~20个字符之间')])
    remember = BooleanField('记住我')
    submit = SubmitField('登陆')


class Change_Password(FlaskForm):
    oldpassword = PasswordField('请输入原密码',validators=[DataRequired()])
    newpassword = PasswordField('新密码',validators=[DataRequired(),Length(6,20,message="密码长度必需在6-20个字符之间")])
    confirmPassword = PasswordField('确认密码', validators=[EqualTo('newpassword', message='两次密码不一致')])
    submit = SubmitField('确认修改')

class Change_Email(FlaskForm):
    newemail = StringField("请输入你要修改的新邮箱",validators=[Email(message="邮箱格式不正确，请从新输入")])
    submit = SubmitField('确认修改')


class UploadForm(FlaskForm):
    icon  = FileField("选择要上传的头像",validators=[FileRequired('选择上传文件'),FileAllowed(photos,message='只能上传图片')])
    submit = SubmitField('确认上传')