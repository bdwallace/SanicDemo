from datetime import datetime, date
from uuid import UUID


def str2byte(_str):
    """
    str to bytes
    :param _str:
    :return:
    """
    return bytes(_str, encoding='utf8')


def byte2str(_bytes):
    """
    bytes to str
    :param _str:
    :return:
    """
    return str(_bytes, encoding="utf-8")


def datatime_serialize(data):
    replica = []
    for item in data:
        tmp = item
        for key, val in item.items():
            if type(val) == datetime:
                tmp[key] = val.strftime('%Y-%m-%d %H:%M:%S')
        replica.append(tmp)
    return replica

def date_serialize(data):
    replica = []
    for item in data:
        tmp = item
        for key, val in item.items():
            if type(val) == date:
                tmp[key] = val.strftime('%Y-%m-%d')
        replica.append(tmp)
    return replica

def uuid_serialize(data):
    replica = []
    for item in data:
        tmp = item
        for key, val in item.items():
            if type(val) == UUID:
                tmp[key] = str(val)
        replica.append(tmp)
    return replica


def bool2str(key, reflect, data):
    """
    :param key: 转换的键值,字符串类型
    :param reflect: 布尔映射关系， 字典数据类型
    :param data: 数据，列表嵌套字典数据类型
    :return:
    """
    replica = []
    for item in data:
        tmp = item
        for k, v in item.items():
            if k == key:
                tmp[k] = reflect[v]
        replica.append(tmp)
    return replica


def cst2utc(date_str):
    """
    CST时间字符串转换为datetime时间格式
    :return:
    """
    date_fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    return datetime.strptime(date_str, date_fmt)

if __name__ == "__main__":
    pass
