from django.shortcuts import render
from .models import Permission
from redis import Redis
from django.conf import settings
from django.core.cache import cache
from .models import Article
import logging
rds = Redis(**settings.REDIS)
logger = logging.getLogger('statistic')

def page_cache(timeout):
    def wrap1(view_func):
        def wrap2(request,*args,**kwargs):
            key = 'PAGES-%s' % request.get_full_path()
            # print('*******',key)
            #从缓存中去出response
            response = cache.get(key)
            if response is not None:
                # print("!!!!!!!!!!!!!")
                return response
            else:
                # print('return from view')
                response = view_func(request,*args,**kwargs)
                #将结果添加到缓存
                cache.set(key,response,timeout)
                return response
        return wrap2
    return wrap1


def check_permission(user,perm_name):
    #检查用户是否有权限
    #Permission类中的id 找出权限为2的对象
    user_perm= Permission.objects.get(id = user.uid) # huang.uid =2 --------uid 2
    need_perm = Permission.objects.get(name = perm_name)
    #管理员权限最大  一般来说user_perm 和need_perm 是相等的
    return user_perm.perm >= need_perm.perm

def permit(perm_name):
    #权限检查装饰器
    def wrap1(view_func):
        def wrap2(request,*args,**kwargs):
            #该方法 返回用户的实例 当前已经登陆的用户
            user = getattr(request,'user',None)
            if user is not  None:
                if check_permission(user,perm_name):
                    return view_func(request,*args,**kwargs)
            return render(request,'404.html')
        return wrap2

    return wrap1




def record_click(article_id,count=1):
    #记录文章的点击数 rds.zincrby自动叠加点击次数
    rds.zincrby('Article-clicks',article_id,count)


def get_top_n_article(number):
    #获取前5的文章
    # article_clicks 格式：
    #   [
    #       (b'3', 725.0),
    #       (b'4', 512.0),
    #       (b'2', 456.0),
    #       ...
    #   ] redis可视化界面的件就是Article-clicks
    # 从 Redis 取出排行数据其中成员的位置按score值递减(从大到小)来排列
    article_clicks = rds.zrevrange('Article-clicks',0,number,withscores=True)
    # 数据类型转换整形
    article_clicks = [[int(aid),int(click)] for aid,click in article_clicks]
    #文章id
    aid_list = [d[0] for d in article_clicks]
    # 批量取出文章
    articles = Article.objects.in_bulk(aid_list)
    #转换aid为Article的实例

    for data in article_clicks:
        # print("a**************", data)

        aid = data[0]
        data[0] = articles[aid]
        # print("vv**************", data[0])
        # 返回的数据格式
        #    [
        #        [Article(6), 725],
        #        [Article(2), 251],
        #        [Article(9), 312],
        #    ]
    return article_clicks



def statistic(view_func):
    def wrap(request,*args,**kwargs):
        response = view_func(request,*args,**kwargs)
        if response.status_code == 200:
            #request.META 可以请求 request.META ip地址  HTTP_USER_AGENT，请求头
            ip = request.META['REMOTE_ADDR']
            aid = request.GET.get('aid')
            logger.info('%s %s' %(ip,aid))

        return response
    return wrap
