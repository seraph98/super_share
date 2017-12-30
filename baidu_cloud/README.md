整个的业务流程是
首先获得查询页面的结果
然后通过get_total_page_info函数， 获得所有页面的url(max = 10)
根据任务分配函数， 将各个页面分配到不同的deal_html函数中

在deal_html函数中， 还需要


关于分享链接:(在请求链接的时候， 需要指明allow_redirects=False)
错误的链接有以下几种:
1. 访问的页面不存在404错误 ex: http://pan.baidu.com/s/1slFee21
2. 访问的链接已经失效 ex: https://pan.baidu.com/s/1o6Ey8Sq


有效的链接有一下几种:
1. 可以直接得到的 ex: http://pan.baidu.com/s/1slFee2T
2. 需要密码 ex: https://pan.baidu.com/s/1i4Jl3pF 密码: bxfn

总结: judge_effective函数用来判断链接的有效性。 返回结果为0,1,2。 其中0表示错误的链接， 
    1表示可以直接打开的链接， 2表示需要密码的链接
    至于判断过程如下所示:
        首先根据返回结构是否需要转发(status_code==302), 如果转发的路径是404，则返0。 然后
        根据返回的内容判断其余三类