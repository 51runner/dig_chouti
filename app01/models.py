from django.db import models


# Create your models here.


class Userinfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    status = models.BooleanField(default=False)

    admin_type_sigle = models.BooleanField(default=False)

    email = models.EmailField(max_length=32)
    authcode = models.CharField(max_length=32)


# 临时管理注册
class Registertime(models.Model):
    email = models.EmailField(max_length=32)
    Originaltime = models.IntegerField()
    Sendcount = models.IntegerField()


# 文章
class Article(models.Model):
    title = models.CharField(verbose_name="标题", max_length=64)  # 标题
    description = models.CharField(verbose_name="摘要", max_length=128)  # 描述
    content = models.TextField(verbose_name="正文")  # 正文
    img = models.ImageField(verbose_name="图片", upload_to='./static/imgs/')  # 标题小图片
    utime = models.IntegerField()  # 记录发布时间
    imgdescription = models.CharField(max_length=128, null=True)  # 图片描述
    web_url = models.URLField(max_length=32, null=True)

    who = models.ForeignKey("Userinfo")  # 当前文章是哪个人发的
    t = models.ForeignKey("Tags")  # 当前文章属于哪一个类型组

    comment_count = models.IntegerField(default=0)
    favor_count = models.IntegerField(default=0)


# 文章类型
class Tags(models.Model):
    caption = models.CharField(max_length=16)


# 点赞表
class Favor(models.Model):
    user = models.ForeignKey(to="Userinfo", to_field="id")
    news = models.ForeignKey(to="Article", to_field="id")


# 评论表
class Comment(models.Model):
    content = models.CharField(max_length=64)
    user_info = models.ForeignKey("Userinfo",to_field="id")
    news = models.ForeignKey("Article")
    parent = models.ForeignKey("self",related_name='o',null=True)
    ctime = models.DateTimeField(auto_now_add=True,null=True)
