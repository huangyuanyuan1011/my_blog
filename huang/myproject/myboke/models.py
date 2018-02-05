from django.contrib.auth.models import Permission
from django.db import models
from django.contrib.auth.hashers import make_password ,check_password#导入密码加密的包
from django.forms import Form,ModelForm,CharField
from django.utils.functional import cached_property

# Create your models here.
#用户表单
class User(models.Model):
    nickname = models.CharField(max_length=64,unique=True,null=False,blank=False)
    password = models.CharField(max_length=64,null=False,blank=False)
    icon  = models.ImageField()
    age = models.IntegerField()
    sex = models.IntegerField()
    uid = models.IntegerField(default=1)   # 权限分1，2，3 最大为3及

    def save(self):
        #密码哈希加密都是pbkdf2_开头
         if not self.password.startswith('pbkdf2_') or len(self.password) <30:
             self.password = make_password(self.password)
         super().save()

    @property
    def permission(self):
        return Permission.objects.get(id = self.uid)


#校验用户是否有权限
class Permission(models.Model):
    perm = models.IntegerField()
    name  = models.CharField(max_length=64,unique=True)


#注册表单
class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['nickname','password','icon','age','sex']

#登陆表单
class LoginForm(Form):
    nickname = CharField(max_length=64)
    password = CharField(max_length=64)

    def chk_password(self):
        #cleaned_data 就是读取表单返回的值，返回类型为字典dict型
        nickname = self.cleaned_data['nickname']
        password = self.cleaned_data['password']
        print("**************",nickname)

        try:
            user = User.objects.get(nickname=nickname)
            print("sssssasss",user)
            return user,check_password(password,user.password)
        except:
            return None, False



class Article(models.Model):
    title = models.CharField(max_length=128)
    data = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    @property
    def tags(self):
        #从文章标签中过滤标签的ID
        article_tags = ArticleTags.objects.filter(aid=self.id).only('tid')
        tid_list = [at.tid for at in article_tags]
        return Tag.objects.filter(id__in=tid_list)
    def update_article_tags(self,tag_names):
        old_tags_names = set(tag.name for tag in self.tags)
        new_tags_names = set(tag_names) - old_tags_names
        need_delete = old_tags_names - set(tag_names)
        #列子
        # print(set((2, 3, 4, 5)) - set((1, 2, 3, 4)))
        # print(set((1, 2, 3, 4)) - set((2, 3, 4, 5)))
        #创建新的关系
        Tag.create_new_tags(new_tags_names,self.id)
        #删除就关系
        need_delete_tids = [t.id for t in Tag.objects.filter(name__in=need_delete)]
        articletags = ArticleTags.objects.filter(tid__in=need_delete_tids)
        for atag in articletags:
            atag.delete()


class Comment(models.Model):
    aid = models.IntegerField()
    name = models.CharField(max_length=128,blank=False,null=False)
    data = models.DateTimeField(auto_now_add=True)
    content = models.TextField()


class Tag(models.Model):
    name = models.CharField(max_length=32,unique=True,blank=False,null=False)

    @classmethod
    def create_new_tags(cls,tag_names,aid):
        #创建Tag
        # 取出已存在的 tags 取出tags的name
        exist_tags = cls.objects.filter(name__in=tag_names).only('name')
        #取出tags的name
        exist = [t.name for t in exist_tags]
        # 去除已存在的 tags
        new_tags = set(tag_names)-set(exist)
        # 生成带创建的 Tag 对象列表
        new_tags = [cls(name=n) for n in new_tags]
        # 批量创建
        cls.objects.bulk_create(new_tags)

        #建立与Aritcle的关系
        tags = cls.objects.filter(name__in=tag_names)
        for t in  tags:
            ArticleTags.objects.update_or_create(aid=aid,tid=t.id)
        return tags

    @cached_property
    def articles(self):
        aid_list = [at.aid for at in ArticleTags.objects.filter(tid=self.id).only('aid')]
        return Article.objects.filter(id__in =aid_list)

class ArticleTags(models.Model):
    aid = models.IntegerField() #article ID
    tid = models.IntegerField() #标签ID