import requests
import re
from baidu_cloud.baidu_cloud_util import judge_effective, get_target_url, find_info
from util.util import get_url_of_host_page

if __name__ == '__main__':
    url1 = 'https://www.baidu.com/s?wd=雷神3%20百度云盘分享'
    url2 = 'https://www.baidu.com/s?wd=%E9%9B%B7%E7%A5%9E3%20%E7%99%BE%E5%BA%A6%E4%BA%91%E7%9B%98%E5%88%86%E4%BA%AB&pn=10&oq=%E9%9B%B7%E7%A5%9E3%20%E7%99%BE%E5%BA%A6%E4%BA%91%E7%9B%98%E5%88%86%E4%BA%AB&ie=utf-8&rsv_pq=ee80acae000091d3&rsv_t=811aBVRmP1JVTDyqFH8wnyLxZgGASdjPWPan%2F2rmFo%2Bag%2BlPi1%2BtLDHoEnI'
    url3 = 'https://www.baidu.com/s?wd=%E9%9B%B7%E7%A5%9E3%20%E7%99%BE%E5%BA%A6%E4%BA%91%E7%9B%98%E5%88%86%E4%BA%AB&pn=20&oq=%E9%9B%B7%E7%A5%9E3%20%E7%99%BE%E5%BA%A6%E4%BA%91%E7%9B%98%E5%88%86%E4%BA%AB&ie=utf-8&rsv_pq=ee80acae000091d3&rsv_t=811aBVRmP1JVTDyqFH8wnyLxZgGASdjPWPan%2F2rmFo%2Bag%2BlPi1%2BtLDHoEnI'
    url4 = 'http://www.baidu.com/link?url=miqGJ8vBaKeZwWirgM4ie3ExMjDgZjrlGlxD9KU2Ji1_ufqPsaqoIkBL5bZyDxAtrOF9f3mqlXwsqcDuJVLYuK'
    # print(get_url_of_host_page(url2))
    print(get_target_url(url4))