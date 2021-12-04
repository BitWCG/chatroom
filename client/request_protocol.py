from config import *

class RequestProtocol(object):
    """客户端请求字符串构造"""

    @staticmethod
    def request_login_result(username,password):
        """0001|user1|111111     类型|账号|密码
        :param username: 账号
        :param password: 密码
        :return: 拼接后的字符串
        """

        return DELIMITER.join([REQUEST_LOGIN,username,password])

    @staticmethod
    def request_chat(username,message):
        """0002|user1|msg     类型|账号|消息内容"""

        return DELIMITER.join([REQUEST_CHAT,username,message])