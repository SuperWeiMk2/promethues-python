#!/bin/python
##coding=utf-8
import requests
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Gauge
from flask import Response, Flask


# 定义函数，返回接口响应码
def statusCode(url):
    try:
        url = url
        response = requests.post(url)
        return response.status_code
    # 加了个捕获异常，是因为如果后端服务挂掉的话，会报错connect refused。如果出现666，说明后端服务挂了
    except:
        return 666


muxCode = statusCode('自己的监控的url')
manageCode = statusCode('自己监控的url')

# 起个flask接口
app = Flask(__name__)

# 定义一个仓库，存放数据
REGISTRY = CollectorRegistry(auto_describe=False)
muxStatus = Gauge("mux_api_21", "Api response stats is:", registry=REGISTRY)
manageStatus = Gauge("manage_api_21", "Api response stats is:", registry=REGISTRY)


# 定义路由
@app.route("/metrics")
def apiResponse():
    muxStatus.set(muxCode)
    manageStatus.set(manageCode)
    return Response(prometheus_client.generate_latest(REGISTRY), mimetype="text/plain")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3531)
