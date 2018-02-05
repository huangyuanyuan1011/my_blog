from app.extensions import mail
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread

# 异步发送邮件
def async_send_mail(app,msg):
    # 发送邮件需要程序上下文，新的线程没有上下文，需要手动创建
    with app.app_context():
        # 发送邮件
        mail.send(message=msg)

# 封装函数，发送邮件
def send_mail(to,subject,template,**kwargs):
    #根据current_app获取当前的实例
    app = current_app._get_current_object()
    #创建邮件的对象
    msg =Message(subject=subject,recipients=[to],sender=app.config["MAIL_USERNAME"])
    #浏览器打开邮件显示的内容
    msg.html= render_template(template+'.html',**kwargs)
    #终端接收邮件显示的内容
    msg.body= render_template(template+'.txt',**kwargs)

    #创建线程
    thr = Thread(target=async_send_mail,args=[app,msg])
    #启动线程
    thr.start()
    return thr