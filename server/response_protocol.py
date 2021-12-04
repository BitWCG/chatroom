#  将相应返回的东西拼接成约定的格式

from config import *


class ResponseProtocol(object):
    """服务器处理返回字符串"""

    @staticmethod
    def response_login_result(result, nickname, username, is_runnign):
        """
        生成用户登录的结果字符串
        :param result: 0 fail，1 success
        :param nickname:
        :param username:
        :return:
        """
        return DELIMITER.join([RESPONSE_LOGIN_RESULT, result, nickname, username, is_runnign])

    @staticmethod
    def response_chat(nickname, messages):
        """
        生成返回给用户的消息字符串
        :param messages:
        :param nickname:
        :return:
        """
        return DELIMITER.join([RESPONSE_CHAT, nickname, messages])
