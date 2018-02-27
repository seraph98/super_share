import sys
sys.path.append('/home/server/super_share')
sys.path.append('/home/gavin/workspace/python/super_share')
sys.path.append('/home/server/super_share/web')
sys.path.append('/home/gavin/workspace/python/super_share/web')
import requests, json

from util.test_util import auto_get_headers_for_vip
from youku.youku_util import gx, aqyba


def get_html_and_parse(url, fun):
    headers = auto_get_headers_for_vip(url)
    if headers is None:
        return []
    result = requests.get(url, headers=headers)
    result.encoding = 'utf-8'
    return fun(result.text)


def main():
    ls = []
    aqyba_url = 'http://www.aqyba.com/'
    ls.extend(get_html_and_parse(aqyba_url, aqyba))
    gx_url = 'http://www.iqyhygx.com/forum-39-1.html'
    ls.extend(get_html_and_parse(gx_url, gx))
    return ls


if __name__ == '__main__':
    main()