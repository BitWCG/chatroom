from server_socket import ServerSocket
from socket_wrapper import SocketWrapper
from threading import Thread
from config import *
from response_protocol import *
from db import DB


class Server(object):

    def __init__(self):
        self.server_socket = ServerSocket()
        # 创建请求的type和方法关联的字典
        self.request_handle_function = {}
        self.register(REQUEST_CHAT, self.request_chat_handle)
        self.register(REQUEST_LOGIN, self.request_login_handle)
        # 创建保存当前用户的字典
        self.clients = {}
        # 初始化数据库
        self.db = DB()

    def register(self, request_type, handle_function):
        # 注册消息类型和处理函数到字典里
        self.request_handle_function[request_type] = handle_function

    def startup(self):

        while True:
            # 接收客户端连接
            print("打开连接")
            soc, addr = self.server_socket.accept()
            print("已建立连接" + addr[0] + ':' + str(addr[1]))

            # 使用套接字生成包装对象
            client_soc = SocketWrapper(soc)
            # 正常开启线程
            # t = Thread(target=self.request_handle, args=(client_soc, addr))
            # t.start()
            # 使用匿名函数的形式开启线程，增加可视性
            Thread(target=lambda: self.request_handle(client_soc, addr)).start()

    def request_handle(self, client_soc, addr):
        while True:
            # 接收消息
            # recv_data = soc.recv(512)
            data = client_soc.recv_data()
            print(data)
            if not data:
                self.remove_offline_user(client_soc)
                client_soc.close()
                break

            # 解析消息
            parse_data = self.parse_request_data(data)
            # 分析请求类型，根据请求类型调用不同的处理函数
            # if parse_data['request_type'] == REQUEST_LOGIN:
            #     self.request_login_handle()
            # elif parse_data['request_type'] == REQUEST_CHAT:
            #     self.request_chat_handle()

            handle_function = self.request_handle_function.get(parse_data['request_type'])

            if handle_function:
                handle_function(client_soc, parse_data)

            # 发送消息
            # soc.send('已成功建立连接'.encode('utf-8'))
            # client_soc.send_data('已接收到客户端{}的消息：{}'.format(addr, data))

    def remove_offline_user(self, client_soc):
        """移除不在线的用户"""
        print("关闭客户端连接")
        for username, info in self.clients.items():
            if info['sock'] == client_soc:
                print(self.clients)
                del self.clients[username]
                print(self.clients)
                break


    def parse_request_data(self, data):
        """
        解析客户端发送来的数据
        登录请求：0001|username|password
        消息请求：0002|username|messages
        """
        # 用我们config中规定好的分隔符进行分割
        request_data = data.split(DELIMITER)
        # 将信息保存在一个字典中
        data_dict = {}
        data_dict['request_type'] = request_data[0]

        if data_dict['request_type'] == REQUEST_LOGIN:
            # 用户请求登录
            data_dict['username'] = request_data[1]
            data_dict['password'] = request_data[2]

        elif data_dict['request_type'] == REQUEST_CHAT:
            # 用户发送信息
            data_dict['username'] = request_data[1]
            data_dict['messages'] = request_data[2]

        return data_dict

    def request_login_handle(self, client_soc, parse_data):
        print("收到登录请求，准备处理")
        # 获取账号密码
        username = parse_data['username']
        password = parse_data['password']
        # 标志用户是否已经登录
        is_running = '0'
        # 验证账号密码正确性
        ret, nickname, username = self.check_user_login(username, password)
        # 登陆成功需要保存当前用户
        if ret == '1':
            if username in self.clients.keys():
                ret = '0'
                is_running = '1'
            self.clients[username] = {'sock': client_soc, 'nickname': nickname}

        # 拼接需要返回的登陆状态等信息
        response_text = ResponseProtocol.response_login_result(ret, nickname, username, is_running)
        # 发送给客户端
        client_soc.send_data(response_text)

    def request_chat_handle(self, client_soc, parse_data):
        print("收到聊天请求，准备处理")
        print(parse_data)
        a = self.clients
        # 获取用户昵称和message
        username = parse_data['username']
        messages = parse_data['messages']
        nickname = self.clients[username]['nickname']

        # 拼接返回数据
        msg = ResponseProtocol.response_chat(nickname,messages)

        # 转发给当前用户clients
        for user, info in self.clients.items():
            if client_soc == info['sock']:
                continue
            info['sock'].send_data(msg)
            print("发送给客户端"+msg)


    def check_user_login(self, username, password):
        """判断用户账号密码正确性"""

        # 在数据库中查询用户信息
        statement = "select * from users where user_name = '{}'".format(username)
        response_result = self.db.get_one(statement)
        print(response_result)
        ret = "0"
        db_nickname = ""
        # 若没有查到则返回失败
        if response_result == 'NULL':
            return ret, db_nickname, username
        # 若密码不正确则返回失败
        db_nickname = response_result.get('user_nickname')
        if password != response_result.get('user_password'):
            db_nickname = ""
            return ret, db_nickname, username
        # 否则返回成功
        ret = "1"
        return ret, db_nickname, username

if __name__ == '__main__':
    Server().startup()
