import sys
import time
sys.path.append('../')
from baidu_cloud import baidu_cloud_main
from wx.sql import *
from selenium import webdriver


#写入公众号
# ls规则[[资源名, 链接, 链接...],[]]
def write_in(ls):
    driver = webdriver.Firefox()
    driver.get('https://mp.weixin.qq.com/')
    driver.find_element_by_name("account").send_keys("2296685742@qq.com")
    driver.find_element_by_name("password").send_keys("15305562330yfl")
    driver.find_element_by_class_name("btn_login").click()
    time.sleep(13)
    print(driver.current_url)
    driver.find_element_by_xpath('//a[contains(@data-id,10006)]').find_element_by_class_name('weui-desktop-menu__name').click()
    driver.find_element_by_link_text('关键词回复').click()
    for nls in ls:
        name = nls[0]
        links = nls[1:]
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div[1]/div[2]/button').click()
        driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/div[1]/div[1]/div/div/span/input').send_keys(name)
        driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/div[1]/div[2]/div/div/span/input').send_keys(name)
        driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/div[1]/div[3]/div/div/div[1]/button').click()
        driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/div[1]/div[3]/div/div/div[1]/div/ul/li[2]').click()
        driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/div[1]/div[3]/div/div/div[3]/div[1]/div/div[2]/div/div/div/div[1]').click()
        temp_str = ''
        for link in links:
            temp_str = link + '\n' + temp_str
        driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/div[1]/div[3]/div/div/div[3]/div[1]/div/div[2]/div/div/div/div[1]').send_keys(temp_str)
        driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/div[1]/div[3]/div/div/div[3]/div[1]/div/div[3]/button[1]').click()
        driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/div[2]/button[1]').click()
        time.sleep(1.5)
    driver.close()


# 获得资源链接并且存入数据库
def search_link(names):
    l = len(names)
    ls = []
    for name in names:
        print(l)
        link, link_ps = baidu_cloud_main.main(name)
        if len(link) == 0:
            continue
        ls.append([name]+list(link))
        l = l - 1
    save(ls)
    return ls


# 从数据库得到资源链接
# 返回ls
def get_link():
    return get_all()


# 获得电影名
def get_movie_name():
    return ['记忆裂缝', '禁闭岛', '记忆碎片', '入侵脑细胞', '玩命记忆', '源代码', '罗马不设防', '辛德勒名单', '现代启示录', '西线无战事', '战争与和平', '奔腾年代',
            '放牛班的春天', '风雨哈佛路', '海上钢琴师', '荒岛余生', '蓝色大门', '老男孩', '小时代', '中国合伙人',  '阿凡达', '安德的游戏', '超体', '第九区','独立日',
            '第五元素', '钢铁侠系列', '火星救援', '黑客帝国', '黑衣人系列', '回到未来系列', '十二只猴子', '少数派报告', '生化危机系列']
    pass


if __name__ == '__main__':
    movie_names = rmredundant(get_movie_name())
    ls = search_link(movie_names)
    write_in(ls)

