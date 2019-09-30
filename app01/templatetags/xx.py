# -*- coding: UTF-8 -*-
# _Author:Rea
from django import template
from django.utils.safestring import mark_safe
from app01 import models

register = template.Library()


@register.simple_tag
def my_simple_time(v1, v2):
    cuurenttime = v1 - v2
    return int(cuurenttime / 60)


"""
<a href="#" class="recommend" title="推荐" n_id="{{ item.id }}">
    <span class="hand-icon icon-recommend dianzan" news_id="{{ item.id }}"></span>
    <b>{{ item.favor_count }}</b>
</a>
"""


@register.simple_tag
def my_faover(news_id, user_id, favor_count):

    """

    :param news_id: 新闻ID
    :param user_id: 用户ID
    :return:
    """
    status = []
    try:
        if models.Favor.objects.filter(user_id=str(user_id["id"]), news_id=str(news_id)).count():
            status = """
            <a href="#" class="recommend" title="推荐" n_id="{}">
                <span class="hand-icon icon-recommend dianzan" news_id="{}"></span>
                <b>{}</b>
            </a>
            """.format(news_id, news_id, favor_count)
        elif models.Userinfo.objects.filter(id=str(user_id["id"])).count():
            status = """
            <a href="#" class="recommend" title="推荐" n_id="{}">
                <span class="hand-icon icon-recommend" news_id="{}"></span>
                <b>{}</b>
            </a>
            """.format(news_id, news_id, favor_count)
        else:
            status = """
            <a href="#" class="recommend" title="推荐" n_id="{}">
                <span class="hand-icon icon-recommend" news_id="{}"></span>
                <b>{}</b>
            </a>
            """.format(news_id, news_id, favor_count)
    except Exception:
        status = """
        <a href="#" class="recommend" title="推荐" n_id="{}">
            <span class="hand-icon icon-recommend" news_id="{}"></span>
            <b>{}</b>
        </a>
        """.format(news_id, 0, favor_count)

    return mark_safe(status)
