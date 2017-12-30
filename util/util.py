import requests
from bs4 import BeautifulSoup

from util.base_util import deal_query, get_target_url, deal_html, get_host, get_base_headers, fix_header, exce_time, \
    self_get_requests


def auto_get_headers(url, timeout=7):
    headers = get_base_headers(url)
    result = self_get_requests(url, headers=headers, timeout=timeout)
    if result is None:
        print('得到头信息时超时:'+url)
        return headers
    if result.status_code == 200 and result.headers.get('Set-Cookie') is not None:
        headers = fix_header(headers, result)
    while result.status_code == 403:
        headers = fix_header(headers, result)
        result = self_get_requests(url, headers=headers, timeout=timeout)
        if result is None:
            print('得到头信息时超时:'+url)
            return headers
    result.encoding = 'utf-8'
    return headers


def get_host_url_list(key_word, timeout=7):
    base_url = 'https://www.baidu.com/s?wd='
    url = deal_query(base_url + key_word)
    headers = auto_get_headers(url)
    result = self_get_requests(url, headers=headers, timeout=timeout)
    if result is None:
        print('百度搜索超时:'+url)
        return list()
    result.encoding = 'utf-8'
    html = result.text
    soup = BeautifulSoup(html, 'lxml')
    page = soup.find(id='page')
    als = page.find_all('a')  #找到链接列表
    ls = []
    for a in als:
        temp_url = 'https://www.baidu.com'+a.get('href')
        target_url = get_target_url(temp_url)
        if target_url is not  None:
            ls.append(target_url)
    ls.insert(0, url)
    return ls


def get_url_of_host_page(url, timeout=7):
    page = get_info_page(url, timeout=timeout)
    ls = deal_html(page)
    return ls


def get_info_page(target_url, timeout=7):
    # 对于百度搜索结果中的一些链接而言， 部分链接可能无法reach， 存在的原因有多种，比如防火墙等, 所以预先做好超时处理
    # todo 测试链接是否通畅, 超时时间设置100秒
    test_result = self_get_requests(target_url, headers = get_base_headers(target_url), timeout = timeout)
    if test_result is None:
        print('超时:'+target_url)
        return ''
    # todo end
    headers = auto_get_headers(target_url)
    result = self_get_requests(target_url, headers=headers, allow_redirects=False, verify=False, timeout=timeout)
    if result is None:
        print('意外超时:'+target_url)
        return ''
    while result.status_code == 307 or result.status_code == 302:
        # 预防措施, 这个while循环可以没有
        target_url = result.headers.get('Location')
        temp_header = headers
        try:
            temp_header['Host'] = get_host(target_url)
        except Exception as e:
            pass
        result = self_get_requests(target_url, headers=temp_header, verify=False, timeout=timeout)
        if result is None:
            print('意外超时:'+target_url)
            return ''
    result.encoding = 'utf-8'
    html = result.text
    return html



