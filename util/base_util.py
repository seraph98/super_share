import sys
sys.path.append('/home/server/super_share')
sys.path.append('/home/gavin/workspace/python/super_share')
sys.path.append('/home/server/super_share/web')
sys.path.append('/home/gavin/workspace/python/super_share/web')
import re, requests
from bs4 import BeautifulSoup
from threading import Thread


# 定义装饰器， try...catch... 超时重传
def exce_time(func):
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as e:
            return None
    return wrapper


# 自定义request.get， 封装try...catch
@exce_time
def self_get_requests(*args, **kw):
    return requests.get(*args, **kw)


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, timeout=0):
        if timeout == 0:
            Thread.join(self)
        else:
            Thread.join(self, timeout)
        return self._return


# 从url中提取出host的值
def get_host(url):
    cp = re.compile(r'//(.*?)/')
    return cp.findall(url)[0]

# 自动动态获取cookie, 组成header防止cookie失效
def get_base_headers(url):
    headers = {
        'Accept': 'text / html, application / xhtml + xml, application / xml; 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en - US, en; q = 0.9',
        'Cache-Control': 'max - age = 0',
        'Connection': 'keep - alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla / 5.0(X11;Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 62.0.3202.94 Safari / 537.36',
    }
    try:
        # headers['Host'] = get_host(url)
        pass
    except Exception as e:
        pass
    return headers


def get_target_url(url, timeout=2):
    headers = get_base_headers(url)
    result = self_get_requests(url, headers=headers, allow_redirects=False, verify=False, timeout=timeout)
    if result is None:
        print('得到目标url超时:'+url)
        return None
    count = 1
    while result.status_code == 307 or result.status_code == 302 or result.status_code == 403:
        if result.status_code == 403:
            headers = fix_header(headers, result)
        else:
            location_url = result.headers.get('Location')
            try:
                headers['Host'] = get_host(location_url)
                url = location_url
            except Exception as e:
                url = 'http://'+get_host(url) +location_url
        result = self_get_requests(url, headers=headers, allow_redirects=False, verify=False, timeout=timeout)
        if result is None:
            print('得到目标url超时:'+url)
            return None
        if count > 2:
            return None
        count = count + 1
    return url


# 处理单个页面数据, 提取出通过百度搜索引擎得到的所有可用链接
# html: 页面信息
# return 页面的中所有可用链接的列表
def deal_html(html):
    soup = BeautifulSoup(html, 'lxml')
    target_block = soup.find_all(class_='result c-container ')
    target_url_ls = []
    for b in target_block:
        target_url_ls.append(b.a.get('href'))
    return target_url_ls


def fix_header(headers, result):
    cookies = result.headers.get('Set-Cookie')
    if cookies is None:
        return headers
    cookie = ''
    ls = cookies.split(',')
    for l in ls:
        str = l.lstrip()
        try:
            if re.match(r'[A-Z]', str[0]):
                cookie = str.split(';')[0] + ';' + cookie
        except Exception as e:
            continue
    if headers.get('Cookie') is None:
        headers['Cookie'] = cookie
    else:
        headers['Cookie'] = headers['Cookie']+cookie
    return headers


# 处理query请求数据(格式化)
def deal_query(query):
    return '%20'.join(re.compile(r'\s+').split(query))


if __name__ == '__main__':
    pass
