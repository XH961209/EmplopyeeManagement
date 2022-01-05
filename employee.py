from myredis.client import redis_client
from mykafka.producer import kafka_producer


MSG_NEW_EMPLOYEE = "new employee|{number}|{name}|{department}"


def register(number, name, department):
    """
    注册一个新员工
    :param number: 工号
    :param name: 姓名
    :param department: 部门
    :return: None
    """
    # TODO:将新员工的信息写入redis

    # TODO:将注册新员工这一事件写入kafka，用户管理系统会从kafka中读取该事件
    #      kafka server应当事先建立一个名为employee-user并且只包含一个分区的topic，用于传递员工管理系统和用户管理系统之间的消息
    #      消息格式为MSG_NEW_EMPLOYEE
    #      消息构造示例: MSG_NEW_EMPLOYEE.format(number="000000", name="alice", department="sale")
