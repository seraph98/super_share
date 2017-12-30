let self_time = 40;
let sto;
function choose(ele) {
    if (ele.getAttribute('class') !== 'top_text_choose') {
        let temp = document.getElementsByClassName('top_text_choose')[0];
        temp.setAttribute('class','top_text');
        ele.setAttribute('class', 'top_text_choose');
        let search = document.getElementById('search_id');
        let id = ele.getAttribute('id');
        search.setAttribute('name', id);
        let title = document.getElementById('main_title_id');
        switch(id){
            case '0':
                title.innerHTML = '百度网盘搜索';
                break;
            case '1':
                title.innerHTML = '迅雷vip搜索';
                break;
            case '2':
                title.innerHTML = '优酷vip搜索';
                break;
            default:
                break
        }
        let result = document.getElementById('result_div_id');
        result.innerHTML = ''
    }
}

function forsearch(ele) {
    begin_power();
    let query = document.getElementById('input_id').value;
    let url = 'http://localhost:5000/baidu_cloud?query='+query;
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState===4 && xmlhttp.status===200) {
            //todo 处理返回值
            let pele = document.getElementById('power_id');
            pele.setAttribute('class', 'no-power');
            document.getElementById('abc').innerHTML = '<span class="span_div">查询中</span><span class="span_div spe" id="sec_id"> 40 </span><span class="span_div">秒</span>';
            let result = xmlhttp.responseText;
            let json = JSON.parse(result);
            let link = json.link;
            let link_ps = json.link_ps;
            let res_ele = document.getElementById('result_div_id');
            for(let i in link){
                let new_node = document.createElement("div");
                new_node.setAttribute('class', 'one_res');
                let new_a1 = document.createElement('a');
                new_a1.setAttribute('href', link[i]);
                new_a1.setAttribute('class', 'baidu_cloud_link');
                new_a1.setAttribute('target', '_blank');
                new_a1.innerHTML = link[i];
                new_node.appendChild(new_a1);
                res_ele.appendChild(new_node)
            }
            for(let i in link_ps){
                let new_node = document.createElement("div");
                new_node.setAttribute('class', 'one_res');
                let new_a1 = document.createElement('a');
                new_a1.setAttribute('href', link_ps[i][0]);
                new_a1.setAttribute('class', 'baidu_cloud_link');
                new_a1.setAttribute('target', '_blank');
                new_a1.innerHTML = link_ps[i][0];
                new_node.appendChild(new_a1);
                let new_a2 = document.createElement('a');
                new_a2.setAttribute('href', link_ps[i][1]);
                new_a2.setAttribute('class', 'baidu_cloud_href');
                new_a2.setAttribute('target', '_blank');
                new_a2.innerHTML = link_ps[i][1];
                new_node.appendChild(new_a2);
                res_ele.appendChild(new_node)
            }
        }
    };
    xmlhttp.open('POST', url, true);
    xmlhttp.setRequestHeader("context-type","text/xml;charset=utf-8");
    xmlhttp.send();
}


function begin_power() {
    let power = document.getElementById('power_id');
    power.setAttribute('class', 'power');
    del_time();
}

function del_time() {
    document.getElementById('sec_id').innerHTML = self_time;
    self_time -- ;
    if (self_time <= 0) {
        document.getElementById('abc').innerHTML = '<span class="span_div">正在处理中...请稍后</span>';
        clearTimeout(sto);
        return;
    }
    sto = setTimeout("del_time()", 1000);
}















