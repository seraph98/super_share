import time
from bs4 import BeautifulSoup
import re, traceback
from multiprocessing import Process, Queue
from util.base_util import get_target_url
from util.util import get_info_page, get_url_of_host_page, auto_get_headers, self_get_requests


def test_cookie():
    url = 'http://pan.baidu.com/s/1hrXwY8k'
    res = judge_effective(url)
    if res == 0:
        return False
    return True


# 判断百度云盘的分享链接是否有效
def judge_effective(link):
    headers = auto_get_headers(link)
    result = self_get_requests(link, headers=headers, allow_redirects=False, timeout=7)
    if result is None:
        print('判断百度云链接是否有效超时:'+link)
        return 0
    if result.status_code == 302 or result.status_code == 307:
        # 如果是转到404页面， 就直接表明是错误的
        if result.headers.get('Location') == '/error/404.html':
            return 0
        return judge_effective(result.headers.get('Location'))
    else:
        result.encoding = 'utf-8'
        title = BeautifulSoup(result.text, 'lxml').title.string
        if title == '百度网盘-链接不存在' or title == '页面不存在':
            return 0
        elif title == '百度网盘 请输入提取密码':
            return 2
        else:
            return 1


# 每个大页面的进程
# html: 页面信息(最多只开三个子进程)
def page_process(url, timeout, fatherQueue):
    target_url_ls = get_url_of_host_page(url, timeout=timeout)
    size = len(target_url_ls)
    l = int(size / 3)
    q = Queue()

    link = set()
    link_ps = set()
    for turl in target_url_ls:
        p = Process(target=info_process, args=([turl], timeout, q))
        p.start()
    for i in range(size):
        try:
            a, b = q.get(timeout = timeout + 5)
        except Exception as e:
            continue
        link = a | link
        link_ps = b | link_ps
    fatherQueue.put((link, link_ps))


    # if l == 0:
    #     print('启动了1个子进程')
    #     p = Process(target=info_process, args=(target_url_ls, q))
    #     p.start()
    #     link, link_ps = q.get()
    #     fatherQueue.put((link, link_ps))
    # elif l == 1:
    #     print('启动了2个子进程')
    #     p1 = Process(target=info_process, args=(target_url_ls[0:3], q))
    #     p2 = Process(target=info_process, args=(target_url_ls[3:size], q))
    #     p1.start()
    #     p2.start()
    #     link1, link_ps1 = q.get()
    #     link2, link_ps2 = q.get()
    #     fatherQueue.put((link1|link2, link_ps1|link_ps2))
    # else:
    #     print('启动了3个子进程')
    #     p1 = Process(target=info_process, args=(target_url_ls[0:3], q))
    #     p2 = Process(target=info_process, args=(target_url_ls[3:6], q))
    #     p3 = Process(target=info_process, args=(target_url_ls[6:size], q))
    #     p1.start()
    #     p2.start()
    #     p3.start()
    #     link1, link_ps1 = q.get()
    #     link2, link_ps2 = q.get()
    #     link3, link_ps3 = q.get()
    #     fatherQueue.put((link1 | link2 | link3, link_ps1 | link_ps2 | link_ps3))


# 每个目标页面中得到云盘链接信息
# 返回的结果有两个， 第一个是没有密码的云盘分享链接， 第二个是有密码的（是一个元组结构， 密码+网址）
def info_process(first_url_list, timeout, q):
    link = set()
    link_ps = set()
    for url in first_url_list:
        url = get_target_url(url, timeout=timeout)
        if url is None:
            continue
        try:
            a, b = find_info(url)
        except Exception as e:
            print('出错了:'+url)
            # traceback.print_exc()
            continue
        link = link | a
        link_ps = link_ps | b
    q.put((link, link_ps))


# 在最后的页面中， 找到云盘信息
# 返回的结果有两个， 第一个是没有密码的云盘分享链接， 第二个是有密码的（是一个元组结构， 密码+网址）
def find_info(url):
    html = get_info_page(url)
    cp = re.compile(r'(http://pan.baidu.com/s/[0-9a-zA-Z]{8}|https://pan.baidu.com/s/[0-9a-zA-Z]{8})')
    ls = cp.findall(html)
    set_url = set(map(get_target_url, set(ls)))
    set_url_ps = set()
    set_url_removing = set()
    for link in set_url:
        res = judge_effective(link)
        if res == 0:
            set_url_removing.add(link)
        if res == 2:
            set_url_removing.add(link)
            set_url_ps.add((link, url))
    for link in set_url_removing:
        set_url.remove(link)
    return set_url, set_url_ps


if __name__ == '__main__':
    print(test_cookie())
