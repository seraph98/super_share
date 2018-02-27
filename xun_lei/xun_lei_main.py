import sys
sys.path.append('/home/server/super_share')
sys.path.append('/home/gavin/workspace/python/super_share')
sys.path.append('/home/server/super_share/web')
sys.path.append('/home/gavin/workspace/python/super_share/web')
import requests, json

from util.test_util import auto_get_headers_for_vip
from util.util import auto_get_headers
from xun_lei.xun_lei_util import fxds, xlfans


def get_html_and_parse(url, fun):
    headers = auto_get_headers_for_vip(url)
    if headers is None:
        return []
    result = requests.get(url, headers=headers)
    result.encoding = 'utf-8'
    return fun(result.text)


def main():
    ls = []
    fxds_url = 'http://www.fenxiangdashi.com/xunlei/'
    ls.extend(get_html_and_parse(fxds_url, fxds))
    xlfans_url = 'http://xlfans.com/archives'
    ls.extend(get_html_and_parse(xlfans_url, xlfans))
    for l in ls:
        print(l)
    return ls


if __name__ == '__main__':
    main()