import sqlite3
import sys
sys.path.append('../')

def __init__():
    pass

#实现数据的保存。 用来保存已经存入的链接
# ls规则[[资源名, 链接, 链接...],[]]
def save(ls):
    conn = sqlite3.connect('wx_movie.db')
    cursor = conn.cursor()
    for nls in ls:
        name = nls[0]
        links = nls[1:]
        for link in links:
            cursor.execute('insert INTO user (name, link) VALUES (?,?)', (name, link))
    cursor.close()
    conn.commit()
    conn.close()


# 去除重复的资源名
# ls规则[资源名, 资源名...]
def rmredundant(ls):
    st = set(ls)
    return st - set(get_all_name())


# 得到所有的资源名
def get_all_name():
    conn = sqlite3.connect('wx_movie.db')
    cursor = conn.cursor()
    cursor.execute('select name from user GROUP BY name')
    values = cursor.fetchall()
    return [x[0] for x in values]


# 得到所有列表
# 返回ls
# ls规则[[资源名, 链接, 链接...],[]]
def get_all():
    conn = sqlite3.connect('wx_movie.db')
    cursor = conn.cursor()
    ls = []
    names = get_all_name()
    for name in names:
        cursor.execute('SELECT link FROM user WHERE name = ?', (name, ))
        links = [x[0] for x in cursor.fetchall()]
        ls.append([name] + links)
    return ls
