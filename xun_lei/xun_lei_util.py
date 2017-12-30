from bs4 import BeautifulSoup

from util.test_util import auto_get_headers_for_vip
from util.util import auto_get_headers
import requests
import re


#http://www.fenxiangdashi.com/xunlei/ 解析
def fxds(html):
    soup = BeautifulSoup(html, 'lxml')
    ul = soup.find(class_='articleCon pt20')
    lis = ul.find_all('li')[0:3]
    ls = []
    for l in lis:
        main_url = 'http://www.fenxiangdashi.com'+l.find('a').get('href')
        headers = auto_get_headers_for_vip(main_url)
        if headers is None:
            continue
        result = requests.get(main_url, headers=headers)
        result.encoding = 'utf-8'
        html = result.text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find(class_='article-content')
        info = str(content)
        ls.extend(re.findall(r'账号：(.+?) 密码：(.+?)<br/>', info))
    return ls


# http://xlfans.com/archives 解析
def xlfans(html):
    soup = BeautifulSoup(html, 'lxml')
    ul = soup.find(class_='content-wrap')
    lis = ul.find_all(class_='excerpt')[0:3]
    ls = []
    for l in lis:
        main_url = l.find('a').get('href')
        headers = auto_get_headers_for_vip(main_url)
        if headers is None:
            continue
        result = requests.get(main_url, headers=headers)
        result.encoding = 'utf-8'
        html = result.text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find(class_='article-content')
        info = str(content)
        ls.extend(re.findall(r'账号：(.+?) 密码：(.+?)<br/>', info))
    return ls



















