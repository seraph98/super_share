import sys
sys.path.append('/home/server/super_share')
sys.path.append('/home/gavin/workspace/python/super_share')
sys.path.append('/home/server/super_share/web')
sys.path.append('/home/gavin/workspace/python/super_share/web')
from bs4 import BeautifulSoup

from util.test_util import auto_get_headers_for_vip
from util.util import auto_get_headers
import requests
import re


#http://www.aqyba.com/ 解析
def aqyba(html):
    soup = BeautifulSoup(html, 'lxml')
    ul = soup.find(class_='content')
    lis = ul.find_all(class_='excerpt excerpt-one')[0:3]
    ls = []
    for l in lis:
        main_url = l.find('h2').find('a').get('href')
        headers = auto_get_headers_for_vip(main_url)
        if headers is None:
            continue
        result = requests.get(main_url, headers=headers)
        result.encoding = 'utf-8'
        html = result.text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find(class_='article-content')
        info = str(content)
        ls.extend(re.findall(r'优酷账号:(.+)密码:(.+)<br/>', info))
    return ls


# http://vip.vipfenxiang.com/yk/ 解析
def gx(html):
    soup = BeautifulSoup(html, 'lxml')
    ul = soup.find(id='threadlisttableid')
    lis = ul.find_all('tbody')[2:6]
    ls = []
    for l in lis:
        main_url = l.find('a').get('href')
        headers = auto_get_headers_for_vip(main_url)
        if headers is None:
            continue
        result = requests.get(main_url, headers=headers)
        result.encoding = 'gbk'
        html = result.text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find(class_='t_fsz')
        info = str(content)
        ls.extend(re.findall(r'优酷账号:(.+?)密码:(.+?)<br/>', info))
    return ls



















