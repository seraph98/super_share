import sys
sys.path.append('/home/server/super_share')
sys.path.append('/home/gavin/workspace/python/super_share')
sys.path.append('/home/server/super_share/web')
sys.path.append('/home/gavin/workspace/python/super_share/web')
from baidu_cloud.baidu_cloud_util import *
from util.util import get_host_url_list, auto_get_headers


def get_html(url, encoding='utf-8', timeout=7):
    headers = auto_get_headers(url)
    result = self_get_requests(url, headers=headers, timeout=timeout)
    if result is None:
        print('得到html页面超时:'+url)
        return ''
    result.encoding = encoding
    return result.text


# 处理query请求数据(格式化) **********
def deal_query(query):
    return '%20'.join(re.compile(r'\s+').split(query))


# 得到所有一级页面信息
# 返回的是一个列表, 每个元素都是不同页面的url
def get_total_page_info(html):
    soup = BeautifulSoup(html, 'lxml')
    page = soup.find(id='page')
    als = page.find_all('a')  #找到链接列表
    ls = []
    for a in als:
        ls.append('https://www.baidu.com'+a.get('href'))
    return ls


# 任务分配函数, 负责将10个页面列表url分配给10个进程处理
def task_share(ls, timeout=10):
    queue = Queue()
    link = set()
    link_ps = set()
    if len(ls) > 5:
        ls = ls[0:5]
    for url in ls:
        p = Process(target=page_process, args=(url, timeout, queue))
        p.start()
    for i in range(len(ls)):
        a, b = queue.get()
        link = link | a
        link_ps = link_ps | b
    return link, link_ps


# main函数
# 处理页面数据
# 总体设计思想: 当发送一个query之后， 会返回一个页面， 这个页面中有下一页信息， 据此， 我们使用10个进程获取10个页面的信息
# 注意， 对于总页面不足01个页面的查询结果， 则开最大进程即可
# 对于每个页面， 先获取所有的url地址， 然后使用3个进程平均分析页面信息
# 返回Link 和 link_ps
# 客户端+8秒
def main(key_word, timeout=10):
    ls = get_host_url_list(key_word+" 百度云盘分享")
    return task_share(ls, timeout=timeout) #第二个参数是当前页面的主体， 这个也是需要的


if __name__ == '__main__':
    print('程序已启动')
    main("记忆提取")