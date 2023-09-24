# 创建flask应用
from flask import Flask, jsonify
import socket
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter

app = Flask(__name__)

metrics = PrometheusMetrics(app)
app_requests = Counter('app_requests', 'Total number of requests to the Flask app')


@app.route('/check_port/<int:port>')
def check_port(port):
    try:
        # 尝试连接到指定端口
        sock = socket.create_connection(('localhost', port), timeout=1)
        sock.close()
        return f"Port {port} is open"
    except ConnectionRefusedError:
        return f"Port {port} is closed"
    # try:
    #     # 尝试连接到指定端口
    #     sock = socket.create_connection(('localhost', port), timeout=1)
    #     sock.close()
    #     return jsonify({'status': 'open', 'port': port})
    # except ConnectionRefusedError:
    #     return jsonify({'status': 'closed', 'port': port})
    # except Exception as e:
    #     return jsonify({'error': str(e)})


@app.route('/')
def index():
    app_requests.inc()
    return 'Hello, World!'


if __name__ == '__main__':
    check_port.run(debug=True)
