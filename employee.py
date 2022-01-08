import time
from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from common import EMPLOYEE_USER_TOPIC
from common import EMPLOYEE_PROPERTIES
from common import MSG_NEW_EMPLOYEE
from myredis.client import redis_client
from mykafka.producer import kafka_producer
from util.password import random_passwd


app = Flask(__name__)


def on_send_success(record_metadata, result):
    result['success'] = True
    result['debug_info'] = "Successfully send message to topic {}, partition {}, offset {}".\
        format(record_metadata.topic, record_metadata.partition, record_metadata.offset)


def on_send_fail(e, result):
    result['success'] = False
    result['info'] = "Fail to send message with error {}".format(e)


def register_request_is_valid(register_request):
    for prop in EMPLOYEE_PROPERTIES:
        if prop not in register_request.json:
            return False
    return True


@app.route('/employee/api/register', methods=['POST'])
def register():
    if not register_request_is_valid(request):
        abort(400)

    # 为新员工随机生成一个10位的初始密码
    passwd = random_passwd(10)

    # 将新员工的信息写入redis的0号数据库
    number = request.json['number']
    name = request.json['name']
    department = request.json['department']
    key = number
    value = {
        "name": name,
        "department": department,
        "password": passwd
    }
    redis_client.hset(name=key, mapping=value)

    # 将注册新员工这一事件写入kafka，用户管理系统会从kafka中读取该事件
    # kafka server应当事先建立一个名为employee-user并且只包含一个partition的topic，用于传递员工管理系统和用户管理系统之间的消息
    result = {
        "success": False,
        "debug_info": ""
    }
    msg_new_employee = MSG_NEW_EMPLOYEE.\
        format(number=number, name=name, department=department, password=passwd).encode()
    kafka_producer.send(EMPLOYEE_USER_TOPIC, msg_new_employee).\
        add_callback(on_send_success, result=result).\
        add_errback(on_send_fail)
    time.sleep(0.1)
    if result["success"]:
        result["password"] = passwd
        # TODO:将密码以邮件的形式通知用户

    return jsonify(result)


if __name__ == "__main__":
    app.run()
