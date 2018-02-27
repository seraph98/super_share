import sys
sys.path.append('/home/server/super_share')
sys.path.append('/home/gavin/workspace/python/super_share')
sys.path.append('/home/server/super_share/web')
sys.path.append('/home/gavin/workspace/python/super_share/web')
from util.base_util import get_base_headers, self_get_requests, fix_header


def auto_get_headers_for_vip(url):
    headers = get_base_headers(url)
    result = self_get_requests(url, headers=headers, timeout=4)
    if result is None:
        print('得到头信息时超时:'+url)
        return None
    if result.status_code == 200 and result.headers.get('Set-Cookie') is not None:
        headers = fix_header(headers, result)
    while result.status_code == 403:
        headers = fix_header(headers, result)
        result = self_get_requests(url, headers=headers, timeout=4)
        if result is None:
            print('得到头信息时超时:'+url)
            return None
    result.encoding = 'utf-8'
    return headers