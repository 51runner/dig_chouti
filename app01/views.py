from django.shortcuts import render, HttpResponse, redirect
from django.db.models import F
import json
from app01 import models
from django import forms
import random
import time
from app01 import spider
from utils.auth import BaseResponse


# Create your views here.

# 装饰器验证
def auth(func):
    def inner(request, *args, **kwargs):
        if request.session.get('is_login', None) and request.session.get("username"):

            return func(request, *args, **kwargs)
        else:
            return redirect('/index.html')

    return inner


class Login(forms.Form):
    username = forms.CharField(error_messages={"required": '用户名不能为空'})
    password = forms.CharField(error_messages={"required": '密码不能为空！'})
    # authcode = forms.IntegerField(error_messages={"required": "验证码不能为空！", "invalid": "验证码格式错误只含数字~"})


class RegisterAuth(forms.Form):
    newusername = forms.CharField(min_length=4, strip=True,
                                  error_messages={"required": '用户名不能为空', 'min_length': '用户名长度不能小4'})
    newemail = forms.EmailField(error_messages={"required": '邮箱不能为空', "invalid": "邮箱格式错误~"})


# 用户在输入用户名Ajax验证
def auth_user(request):
    user_dict = {'username': None, 'status': True}
    if request.method == "GET":
        return redirect('/index.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        if models.Userinfo.objects.filter(username=username).count():
            user_dict['username'] = username
        else:
            user_dict['status'] = False
        return HttpResponse(json.dumps(user_dict))


# 首页 获取验证码
def index(request):
    if request.method == "GET":
        from django.core.handlers.wsgi import WSGIRequest
        print(request.environ["HTTP_USER_AGENT"])

        # 分页
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)

        # 取出数据库 数据总数
        total_count = models.Article.objects.all().count()
        from utils.page import PagerHelper
        obj = PagerHelper(total_count, current_page, '/index.html')
        pager = obj.pager_str()

        status_auth = {'username': request.session.get("username"), 'is_login': request.session.get('is_login')}
        user_id = models.Userinfo.objects.filter(username=status_auth["username"]).values("id").first()
        request.session["user_id"] = user_id

        articles = models.Article.objects.all().order_by("-id")[obj.db_start:obj.db_end].values("id", "title",
                                                                                                "description",
                                                                                                "content",
                                                                                                "img", "utime",
                                                                                                "imgdescription",
                                                                                                "t_id", "t__caption",
                                                                                                "web_url",
                                                                                                "who__username",
                                                                                                "favor_count")
        # [::-1]
        tags = models.Tags.objects.all()
        current_time = time.time()
        # favor_count = models.Userinfo.objects.
        return render(request, 'index.html',
                      {"userinfo": status_auth, "articles": articles, 'tags': tags, "current_time": int(current_time),
                       'str_pager': pager, "user_id": user_id})





    elif request.method == "POST":
        result = {
            'status': True,
            'error': None,
            'data': None,
            'authocede': None,
            'username': None,
            'passowrd': None,
            'messagess': None,
        }

        obj = Login(request.POST)
        if obj.is_valid():
            # clean 是拿到成功的数据为dict类型
            value_dict = obj.clean()
            username = value_dict['username']
            password = value_dict['password']

            # 判断用户名和密码是否存在~
            if models.Userinfo.objects.filter(username=username, password=password).count():
                # 生成随机字符串验证码
                random_int = random.randint(1000, 9999)
                # 验证码并且返回给用户
                result['authocede'] = str(random_int)
                request.session['username'] = username
                request.session['is_login'] = True

                models.Userinfo.objects.filter(username=username).update(authcode=str(random_int))
                result['username'] = username
                result['password'] = password
            else:
                result['status'] = False
                result['username'] = username
                result['passowrd'] = password
                result['messagess'] = "用户名和密码不一致~"

            return HttpResponse(json.dumps(result))
        else:
            error_obj = obj.errors.as_json()
            result['status'] = False
            result['error'] = error_obj

            return HttpResponse(json.dumps(result))


# 登陆验证
def authlogin(request):
    result = {'status': True, 'messages': None}
    if request.method == "GET":
        return redirect('/index.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get("password")
        authcode = request.POST.get('authcode')
        if models.Userinfo.objects.filter(username=username, password=password, authcode=authcode).count():

            pass
        else:
            result['status'] = False
            result['messages'] = "验证码错误~"
        return HttpResponse(json.dumps(result))


# 注册验证
advance_time = 0
auth_code = 0


def register(request):
    global advance_time, auth_code
    ret = {
        'status': True,
        'error_message': None,
        'username': None,
        'success_s': None,
        'authocede': None
    }

    if request.method == "GET":
        return redirect('/index.html')
    elif request.method == "POST":
        obj = RegisterAuth(request.POST)
        if obj.is_valid():
            value_dict = obj.clean()

            # 两个小时之后的时间
            # tow_hours_time = time.time() + 7200
            # if models.Registertime.objects.filter(email=value_dict["email"]).count():
            #     models.Registertime.objects
            #
            # else:
            #     models.Registertime.objects.create(email=value_dict["email"])


            random_int = random.randint(1000, 9999)
            # 验证码并且返回给用户
            advance_time = time.time() + 60
            ret['authocede'] = str(random_int)
            auth_code = str(random_int)

            # 基于session来存储验证码
            request.session["authcode"] = str(random_int)
            # str(random_int)
            ret['username'] = value_dict['newusername']
            request.session['username'] = value_dict['newusername']
            request.session['is_login'] = False



        else:
            error_obj = obj.errors.as_json()
            ret['status'] = False
            ret['error_message'] = error_obj

        # models.Userinfo.objects.create(*userinfo_dict)


        return HttpResponse(json.dumps(ret))


# 注册时间验证
def time_auth(request):
    global advance_time, auth_code

    if request.method == "GET":
        return redirect("/index.html")
    elif request.method == "POST":
        result = {'status': True, "message": None, "userinfo": None, "authcode": None}

        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        authcode = request.POST.get("authcode")
        if request.session.get("authcode") == authcode:
            if advance_time >= time.time():

                userinfo_dict = {
                    'username': username,
                    "password": password,
                    "email": email,
                    "authcode": authcode
                }
                result['authocede'] = request.session.get("authcode")
                # models.Userinfo.objects.create(*userinfo_dict)
                models.Userinfo.objects.create(username=username, password=password, email=email, authcode=authcode)
                request.session['username'] = username
                request.session['is_login'] = True
            else:
                result['message'] = "验证码过期~"
                result['status'] = False
                request.session["authcode"] = ""
        else:
            result["message"] = "验证码错误~"
            result["status"] = False

        return HttpResponse(json.dumps(result))


# 退出登陆

def loginuot(request):
    if request.method == "GET":
        request.session['is_login'] = False
        return redirect("/index.html")
    elif request.method == "POST":
        authusers = {"status": False}
        if request.session['is_login'] == True:
            authusers["status"] = True
        else:
            authusers['status'] = False

        return HttpResponse(json.dumps(authusers))


# 蜘蛛数据 发布文章
def article(request):
    if request.method == "GET":
        return redirect('/index.html')
    elif request.method == "POST":
        res = {'status': True, 'error_message': None}
        try:
            web_url = request.POST.get("web_url")
            title = request.POST.get("title")
            description = request.POST.get("description")
            t_id = request.POST.get("t_id")
            who_id = request.POST.get("who_id")
            data = {
                "title": title,
                "description": description,
                "t_id": t_id,
                "content": description,
                "img": "2016122201.jpg",
                "utime": int(time.time()),
                "imgdescription": "sipder img",
                "web_url": web_url,
                "who_id": who_id,
            }
            models.Article.objects.create(**data)
        except Exception as e:
            res["status"] = False
            res["error_message"] = "缺字段~"

        return HttpResponse(json.dumps(res))


# 查看文章
def getarticle(request, nid):
    if request.method == "GET":
        article = models.Article.objects.filter(id=nid).values("id",
                                                               "title",
                                                               "description",
                                                               "content",
                                                               "img",
                                                               "utime",
                                                               "imgdescription",
                                                               "t_id",
                                                               "t__caption").first()
        # print(article)
        # print(nid)

        return redirect('/index.html')
    elif request.method == "POST":
        return redirect('/index.html')


# 获取文章链接视图
def get_link(request):
    if request.method == "GET":
        res = {"status": True}
        web_url = request.GET.get("web_url")
        web_info = spider.get_url(web_url)

        return HttpResponse(json.dumps(web_info))

    elif request.method == "POST":
        result = {"status": True, "error": None}
        title = request.POST.get("title")
        description = request.POST.get("description")
        t_id = request.POST.get("t_id")
        content = request.POST.get("content")
        imgdesciption = request.POST.get("imgdesciption")
        img = request.session.get("imgname")

        who_id = request.POST.get("who_id")
        add_result_dict = {
            "title": title,
            "description": description,
            "t_id": t_id,
            "content": content,
            "imgdescription": imgdesciption,
            "img": img,
            "utime": int(time.time()),
            "who_id": who_id

        }
        print(add_result_dict)
        models.Article.objects.create(**add_result_dict)

        print(title, description, t_id, content, img, imgdesciption)

        return HttpResponse(json.dumps(result))


import time
import os


def upload_img(request):
    if request.method == "GET":
        result = {"status": True, "error_message": None}
        imgname = request.GET.get("imgname")
        print(imgname)
        if os.path.join('static', 'imgs', imgname):
            path_img = os.path.join('static', 'imgs', imgname)
            s = os.remove(path_img)
            print(request.session.get("imgname"))

            request.session["imgname"] = None
        else:
            result["status"] = False
            result["error_message"] = "图片无存在~"
        return HttpResponse(json.dumps(result))

    elif request.method == "POST":
        result = {'status': True, "img_path": None, "imgname": None, 'error_message': None}
        file_img = request.FILES.get("file_img")
        if file_img:
            file_img.name = str(int(time.time() * 1000)) + '.' + file_img.name.split('.')[-1]
            # 把文件名 存入session
            request.session['imgname'] = file_img.name
            file_path = os.path.join('static', 'imgs', file_img.name)
            f = open(file_path, 'wb')
            for chunk in file_img.chunks():
                f.write(chunk)
            f.close()
            result['img_path'] = file_path
            result['imgname'] = file_img.name
            print(file_img.name, file_path)
        else:
            result['status'] = False
            result['error_message'] = '请上传图片！'
        return HttpResponse(json.dumps(result))


# 后台管理
@auth
def vip(request):
    if request.method == "GET":
        user_id = models.Userinfo.objects.filter(username=request.session.get('username')).values("id").first()
        return render(request, "admin/index.html", {"username": request.session.get('username'), "user_id": user_id})


# 后台管理 个人发布中心
@auth
def viphome(request, vid):
    if request.method == "GET":
        user_id = models.Userinfo.objects.filter(username=request.session.get("username")).values("id").first()
        if user_id["id"] == int(vid):
            request.session["auth_home"] = False
            userinfo = models.Userinfo.objects.filter(id=vid).values("id", "username", "email").first()
            get_article = models.Article.objects.filter(who_id=vid).values("id", "title", "description")[::-1]

            return render(request, "admin/viphome.html",
                          {"userinfo": userinfo, "username": userinfo["username"], "article": get_article})
        else:
            request.session["auth_home"] = True
            return redirect("/admin_profile.html")




            # 访问个人中心装饰器
            # def auth_home(func):
            #     def inner(request, *args, **kwargs):
            #         uid = models.Userinfo.objects.filter(username=request.session.get("username")).values("id").first()
            #         if uid:
            #
            #     return inner


# 删除文章
@auth
def delviphome(request, nid, uid):
    if request.method == "GET":
        models.Article.objects.filter(id=nid).delete()

        link = "/viphome-{}.html".format(uid)
        return redirect(link)


# 后台编辑文章
@auth
def ediviphome(request, nid, uid):
    """

    :param request:
    :param nid: 文章ID
    :param uid: 用户ID
    :return:
    """
    if request.method == "GET":
        tags_list = models.Tags.objects.all().values("id", "caption")
        get_article = models.Article.objects.filter(id=nid).first()
        return render(request, "admin/ediarticle.html", {"tags_list": tags_list, "article": get_article, "uid": uid})
    elif request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        content = request.POST.get("content")
        models.Article.objects.filter(id=nid).update(title=title, description=description, content=content)

        link = "/viphome-{}.html".format(uid)
        return redirect(link)


# 后台个人简介
@auth
def admin_profile(request):
    if request.method == "GET":
        username = request.session.get("username", None)
        userinfo_list = models.Userinfo.objects.all()
        """
        if request.session["auth_home"]:
            # 拦截提示
            request.session["auth_home"] = False
            msg = True
            return render(request, "admin/profile.html",
                          {"userinfo_list": userinfo_list, "username": username, "msg": msg})
        else:
            msg = False
            request.session["auth_home"] = False
            return render(request, "admin/profile.html",
                          {"userinfo_list": userinfo_list, "username": username, "msg": msg})
        """

        msg = False
        return render(request, "admin/profile.html",
                      {"userinfo_list": userinfo_list, "username": username, "msg": msg})


# 可编辑个人信息
@auth
def personal(request, nid):
    if request.method == "GET":
        user_id = models.Userinfo.objects.filter(username=request.session.get("username")).values("id").first()
        if user_id["id"] == int(nid):
            userinfo_list = models.Userinfo.objects.filter(id=nid).first()

            return render(request, "admin/personal.html", {"username": request.session.get("username"),
                                                           "userinfo": userinfo_list})
        else:
            return redirect("/admin_profile.html")

    elif request.method == "POST":
        pass


# 验证密码是否存在
@auth
def auth_pwd(request):
    if request.method == "GET":
        return redirect("/vip.html")
    elif request.method == "POST":
        obj = BaseResponse()
        # result = {"status": True, }
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")
        c = models.Userinfo.objects.filter(id=user_id, password=password).count()
        if c:
            pass
        else:
            obj.status = False
        return HttpResponse(json.dumps(obj.__dict__))


# 点赞
@auth
def favor(request):
    obj = BaseResponse()
    if request.method == "GET":
        news_id = request.GET.get("news_id")
        if models.Favor.objects.filter(news_id=news_id, user_id=str(request.session.get("user_id")["id"])).count():
            models.Favor.objects.filter(news_id=news_id, user_id=str(request.session.get("user_id")["id"])).delete()

            models.Article.objects.filter(id=news_id).update(favor_count=F('favor_count') - 1)
            obj.status = False
        else:
            # 时间判断和点击次数的判断

            models.Favor.objects.create(news_id=news_id, user_id=str(request.session.get("user_id")["id"]))
            models.Article.objects.filter(id=news_id).update(favor_count=F('favor_count') + 1)
            pass
        return HttpResponse(json.dumps(obj.__dict__))

    elif request.method == "POST":
        news_id = request.POST.get("news_id")

        if models.Favor.objects.filter(news_id=news_id, user_id=str(request.session.get("user_id")["id"])).count():
            models.Favor.objects.filter(news_id=news_id, user_id=str(request.session.get("user_id")["id"])).delete()
            models.Article.objects.filter(id=news_id).update(favor_count=F('favor_count') - 1)
        else:
            obj.status = False
        return HttpResponse(json.dumps(obj.__dict__))


# 构建评论数
class Node:
    @staticmethod
    def digui(ret, row):
        for rt in ret:
            if rt['id'] == row['parent_id']:
                row['children'] = []
                rt['children'].append(row)
                return
            else:
                Node.digui(rt["children"], row)

    @staticmethod
    def create_tree(result_comment):
        ret = []
        for row in result_comment:
            # 如果parent_id是空的话就等于没有 也就是跟评论
            if not row['parent_id']:  # None
                row["children"] = []
                ret.append(row)
            else:
                # 是回复的某个评论
                # for i in ret:
                #     if row["parent_id"] == i["id"]:
                #         row["children"] = []
                #         i["children"].append(row)
                #     else:
                #         for j in i["children"]:
                #             pass
                Node.digui(ret, row)

        return ret


# 评论测试
def comment(request):
    news_id = 31
    # for row in comment_list:
    #     print(row.id, row.content, row.user_info.username, row.parent_id)
    comment_lists = models.Comment.objects.filter(news_id=31).values("id", "news_id", "content", "user_info__username",
                                                                     "parent_id")
    result_comment = []
    for item in comment_lists:
        comment_list = {"id": item["id"],
                        "news": item["news_id"],
                        "content": item["content"],
                        "user": item["user_info__username"],
                        "parent_id": item["parent_id"]
                        }
        result_comment.append(comment_list)

    comment_tree = Node.create_tree(result_comment)
    print(comment_tree)

    return HttpResponse("Comment")
