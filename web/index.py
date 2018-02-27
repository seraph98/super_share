from flask import request, Flask, render_template
from baidu_cloud import baidu_cloud_main
from xun_lei import xun_lei_main
from youku import youku_main
import json
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/baidu_cloud', methods=['GET', 'POST', 'OPTIONS'])
def baidu_cloud():
    query = request.args.get('query')
    print(query)
    link, link_ps = baidu_cloud_main.main(query)
    obj = {
        'link': list(link),
        'link_ps': list(link_ps)
    }
    return json.dumps(obj)


@app.route('/xunlei_vip', methods=['GET', 'POST', 'OPTIONS'])
def xunlei_vip():
    ls = xun_lei_main.main()
    obj = {
        'ap': ls
    }
    return json.dumps(obj)

@app.route('/youku_vip', methods=['GET', 'POST', 'OPTIONS'])
def youku_vip():
    ls = youku_main.main()
    obj = {
        'ap': ls
    }
    return json.dumps(obj)


@app.route('/test', methods=['GET', 'POST'])
def test():
    obj = {
        'a': {1,2,3},
        'b': [5,6,7]
    }
    return json.dumps(obj)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
