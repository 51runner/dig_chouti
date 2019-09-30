from django.db import models


# Create your models here.

class Userinfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    status = models.BooleanField(default=False)
    email = models.EmailField(max_length=32)
    authcode = models.CharField(max_length=32)



    u = models.ForeignKey("Usertype")

# 临时管理注册
class Registertime(models.Model):
    email = models.EmailField(max_length=32)
    Originaltime = models.IntegerField()
    Sendcount = models.IntegerField()


class Article(models.Model):
    title = models.CharField(verbose_name="标题", max_length=64)   #标题
    description = models.CharField(verbose_name="摘要", max_length=128)  #描述
    content = models.TextField(verbose_name="正文")  #正文
    img = models.ImageField(verbose_name="图片", upload_to='./static/imgs/')  #标题小图片
    utime = models.IntegerField(max_length=32)  # 记录发布时间
    imgdescription = models.CharField(max_length=128) #图片描述
    commnet_count = models.IntegerField(default=0)  #评论数
    zan = models.IntegerField(default=0) #点赞数量

    t = models.ForeignKey("Tags")  #当前文章属于哪一个类型组
    user = models.ForeignKey("Userinfo")  #当前文章是谁发布的


class Comment(models.Model):
    id_article = models.ForeignKey("Article")  #文章id
    id_sender = models.ForeignKey("Userinfo") #是谁评论的
    content = models.TextField() # 评论的内容
    sendtime = models.IntegerField() #记录评论时间
    equipment = models.CharField(max_length=24)  #用户的设备 app ro pc





# 文章类型
class Tags(models.Model):
    caption = models.CharField(max_length=16)



# 用户类型 超级管理员 管理员 版主 普通用户
class Usertype(models.Model):
    caption = models.CharField(max_length=16)




