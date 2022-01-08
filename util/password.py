import random
import string


def random_passwd(k: int):
    """
    随机生成一个K位密码
    :param k:
    :return: 长度为k的字符串，表示生成的密码
    """
    sequence = string.ascii_letters + string.digits
    return "".join(random.sample(sequence, k))
