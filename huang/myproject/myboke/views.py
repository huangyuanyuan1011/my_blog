from django.shortcuts import render,redirect
from .models import RegisterForm,LoginForm,User,Article,ArticleTags,Tag,Comment
from math import ceil
from .helper import record_click,get_top_n_article,rds,page_cache,permit
from .middleware import AuthenticationMiddleware
from.helper import statistic
import time

# Create your views here.im
import time
# def base(request):
#     return render(request,'base.html')


def register(request):
    register_name = 'register'
    if request.method=="POST":
        flag = 0
       #实例话对象  request.POST获取所有输入的信息  request.FILES 上传的图片
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            flag = 1
            resp = redirect('/login/')
            resp.set_cookie('flag', flag)
            user = form.save(commit=False)
            user.save()
            request.session['userid'] = user.id
            return resp
        else:
            return render(request,'register.html',{'errors':form.errors})
    userid = request.session.get('userid')
    user = None
    if userid is not None:
        user = User.objects.get(id=userid)
    return render(request,'register.html',{'user':user,'register_name':register_name})


def info(request):
   uid = request.session.get('userid')
   if uid is not None:
       user = User.objects.get(id = uid)
       return render(request,'info.html',{'user':user})
   else:
       return redirect('/register/')

def login(request):
    # flag = request.COOKIES.get('flag')
    login_name = "login"
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user,passwd = form.chk_password()
            # print(passwd,user)
            if passwd:
                request.session['userid'] = user.id
                return redirect('/index/')
    user = None
    return render(request,'login.html',{'login_name':login_name, 'user': user})

def logout(request):
    request.session.flush()
    return redirect('/login/')

@page_cache(1)
def index(request):
    #计算总页数
    count = Article.objects.count()
    pages = ceil(count/5)
    page = int(request.GET.get('page',1))
    # page = 0 if page < 1 or page >= (pages + 1) else (page - 1)
    #取出来当前也的文章
    start = (page-1) * 5
    end  =start + 5
    articles = Article.objects.all().order_by('-data')[start:end]
    #取出前5的文章
    top5 = get_top_n_article(5)
    user_id = request.session.get('userid')
    user = None
    if user_id is not None:
        user = User.objects.get(id=user_id)
    return render(request,'index.html',{'articles':articles,'page':page,'pages':range(pages),'user':user,'top5':top5})

def create(request):
    if request.method=="POST":
        #创建文章
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article.objects.create(title=title,content=content)

        #创建tags
        tags = request.POST.get('tags')
        if tags:
            tags = [t.strip() for t in tags.split(',')]
            Tag.create_new_tags(tags,article.id)
        return redirect('/article/?aid=%s'% (article.id))
    userid = request.session.get('userid')
    user = None
    if userid is not None:
        user = User.objects.get(id=userid)
    return render(request,'create.html',{'user':user})
@page_cache(1)
@statistic
def article(request):
    aid =int(request.GET.get('aid',1))
    article = Article.objects.get(id = aid)
    comments = Comment.objects.filter(aid=aid)
    record_click(aid)  #记录点击文章
    userid=request.session.get('userid')
    try:
        user = User.objects.get(id =userid)
    except:
        return redirect('/login/')
    return render(request,'article.html',{
        'article':article,'comments':comments,'tags': article.tags,'user':user
    })
@permit('user')
def comment(request):
    if request.method=="POST":
        name = request.POST.get('name')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))
        # print("********111111111111")
        Comment.objects.create(content=content,aid=aid, name=name)
        return redirect('/article/?aid=%s'% aid)
    return redirect('/index/')
@permit('user')
def editor(request):
    if request.method=='POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))
        # print(aid)
        #把修改后的文章属性保存到模型中
        article = Article.objects.get(id=aid)
        article.title = title
        article.content = content
        article.save()
        tags = request.POST.get('tags')
        if tags:
            tag_names = [t.strip() for t in tags.split(',')]
            # 创建 或更新 或删除
            article.update_article_tags(tag_names)

        return  redirect('/article/?aid=%s'% (article.id))
    else:
        aid = request.GET.get('aid',1)
        article = Article.objects.get(id = aid)
        userid = request.session.get('userid')
        user  = None
        if userid is not  None:
            user = User.objects.get(id = userid)
    return render(request,'editor.html',{'article':article,'user':user})



def search(request):
    if request.method=="POST":
        keyword = request.POST.get('keyword')
        articles = Article.objects.filter(content__contains=keyword)
        # aid = int(request.POST.get('aid'))
        # 计算总页数
        count = Article.objects.count()
        pages = 1
        top5 = get_top_n_article(5)
        userid = request.session.get('userid')
        user = None
        if userid is not None:
            user = User.objects.get(id=userid)
        return render(request,'search.html',{'articles':articles,'top5':top5,'pages':range(pages),'user':user})

@permit('admin')
def delete(request):
    aid = request.GET.get('aid')
    rds.zrem('Article-clicks',aid)
    Article.objects.get(id = aid).delete()
    return redirect('/index/')

import os,random

@permit('user')
def change_icon(request):
    if request.method == "POST":
        userid = request.session.get('userid')
        user = None
        if userid is not None:
            user = User.objects.get(id=userid)
        if request.FILES.get('icons'):
            os.remove('./medias/'+str(user.icon))
            new_icon = request.FILES.get('icons')
            suffix = os.path.splitext(new_icon.name)[1]
            icon_file = random_str() + suffix
            with open('./medias/'+str(icon_file), 'wb') as f:
                for chunks in new_icon.chunks():
                    f.write(chunks)
                user.icon = icon_file
                user.save()
        else:
            return redirect('/info/')
        return redirect('/info/')


def random_str():
    str = "12345678qwertyuioasdfghj"
    return ''.join(random.choice(str) for i in range(14))
