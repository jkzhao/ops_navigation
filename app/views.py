# Create your views here.
import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from app.models import UrlGroup,UrlInfor
import json

def index(request):
    """
    前端展示文件入口
    """
    today = datetime.date.today()
    weekday = get_week_day(datetime.datetime.now())
    return render(request, 'index.html', {"today": today, "weekday": weekday})

def get_week_day(date):
    """
    获取当天是星期几，用来实现页面展示
    """
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]

def serialization_data(request):
    """
    构造数据格式
        list
            dict
                list
                    dict

    从组里取出所有组，然后再根据一对多的关系，通过组获取url的具体信息，属于反向获取数据
    [{"code": "utils", "list": [{"desc": "\u7ebf\u4e0aelk\u65e5\u5fd7\u68c0\u7d22\u7cfb\u7edf", "href": "http://192.168.0.210", "title": "\u7ebf\u4e0aelk\u7cfb\u7edf"}, {"desc": "\u7ebf\u4e0a\u90ae\u7bb1\u5730\u5740\uff0c\u516c\u53f8\u5185\u90e8\u90ae\u7bb1\u767b\u9646\u94fe\u63a5", "href": "http://192.168.0.215", "title": "\u90ae\u7bb1\u5730\u5740"}], "title": "\u751f\u4ea7\u73af\u5883"}, {"code": "staging", "list": [{"desc": "zabbix\u76d1\u63a7\u7cfb\u7edf\uff0c\u53ef\u4ee5\u7cfb\u7edf\u7cfb\u7edf\u548c\u5e94\u7528\u5c42\u7684\u76d1\u63a7\u4fe1\u606f", "href": "http://192.168.0.211", "title": "\u7ebf\u4e0azabbix\u7cfb\u7edf"}], "title": "\u9884\u53d1\u73af\u5883"}, {"code": "testing", "list": [{"desc": "\u8fd0\u7ef4\u5185\u90e8nginx\u7ba1\u7406\u5e73\u53f0", "href": "http://192.168.0.215", "title": "\u7ebf\u4e0anginx\u7ba1\u7406\u5e73\u53f0"}, {"desc": "sdf", "href": "http://192.168.0.212", "title": "\u7ebf\u4e0arundeck"}], "title": "\u6d4b\u8bd5\u73af\u5883"}, {"code": "loading", "list": [{"desc": "\u538b\u6d4b\u73af\u5883\u4ee3\u7801\u53d1\u5e03\u4e4bjenkins\u4e13\u7528", "href": "http://192.168.0.212", "title": "jenkins"}], "title": "\u538b\u6d4b\u73af\u5883"}, {"code": "QA", "list": [{"desc": "qa\u4e13\u7528SmokeTest\u9875\u9762", "href": "http://192.168.0.215", "title": "smoketest"}], "title": "QA\u4e13\u573a"}, {"code": "new_work", "list": [{"desc": "\u4e2a\u4eba\u5f00\u53d1\u673a\u5668\u7533\u8bf7\uff0c\u7528\u4e8e\u4e2a\u4eba\u5199\u4ee3\u7801\u7528\u9014", "href": "http://192.168.0.214", "title": "\u4e2a\u4eba\u5f00\u53d1\u673a\u7533\u8bf7"}, {"desc": "\u7528\u4e8e\u767b\u9646\u7ebf\u4e0b\u3001\u7ebf\u4e0a\u5821\u5792\u673a", "href": "http://192.168.0.215", "title": "\u5821\u5792\u673a\u8d26\u53f7\u7533\u8bf7"}], "title": "\u65b0\u5458\u5de5\u4e0a\u624b"}]
    """
    _group_lists = UrlGroup.objects.all()
    _datas = []
    for group in _group_lists.all():
        if group.group_set.count() > 0:
            _group_template = {"title": "{0}".format(group.group_name), "code": "{0}".format(group.code), "list": []}
            _group = UrlGroup.objects.get(code=group.code)
            for k in _group.group_set.all():
                _url_template = {"title": "{0}".format(k.url_name), "href": "{0}".format(k.url_path),
                                 "desc": "{0}".format(k.url_desc)}
                _group_template["list"].extend([_url_template])
            _datas.extend([_group_template])
    result = json.dumps(_datas)

    return HttpResponse(result)

