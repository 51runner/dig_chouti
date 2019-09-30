# -*- coding: UTF-8 -*-
# _Author:Rea

from bs4 import BeautifulSoup
import requests


def get_url(url):
    res = {"status": True, "description": None, "title": None, "error_messgea": None}
    try:
        web_url = requests.get(url)
        soup = BeautifulSoup(web_url.text, 'lxml')
        title = soup.find("title").text
        description = soup.find_all(attrs={"name": "description"})[0]["content"]
        res["description"] = description
        res["title"] = title
        return res
    except Exception as e:
        res["status"] = False
        return res


if __name__ == '__main__':
    s = get_url("http://taobao.com/")
    print(s)
