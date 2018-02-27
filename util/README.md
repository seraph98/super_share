base_util是为util提供方法的， 暴露给外面的是util

* 约定所有返回的url都必须是target_url, 为了方便管控

这个util文件夹中存放工具, 做一层封装
使用说明:
1. get_host_url_list(key_word)
参数: key_word 查询关键字
返回: 每个主页面的url列表 
2. get_url_of_host_page(url) 
参数: url 根据get_host_url_list返回url列表中的每一项
返回: 每一个主页面中所有url列表
3. get_info_page(url)
参数: url 是2中返回的url中的一个
返回: 页面html
4. auto_get_headers(url)
参数: url是任意一个url, 
返回: 根据url， 自动回一个符合url中host的请求头信息