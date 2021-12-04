import os
import sys
from threading import Thread

from window_login import WindowLogin
from window_chat import WindowChat
from request_protocol import RequestProtocol
from client_socket import ClientSocket

from tkinter.messagebox import showinfo
import logging
from config import *

logging.basicConfig(filename='my.log', level=logging.DEBUG)

class Client(object):

    def __init__(self):
        # 生成登录窗口
        self.window = WindowLogin()
        self.window.reset_button_click(self.clear_input)
        self.window.login_button_click(self.send_login_data)
        self.window.children['password_entry'].bind('<Return>', self.send_login_data)
        self.window.window_close(self.exit)

        # 生成聊天窗口
        self.window_chat = WindowChat()
        self.window_chat.send_button_click(self.send_chat_data)
        # self.window.bind('<Return>', self.window_chat.send_button_click(self.send_chat_data))
        self.window_chat.children['chat_input_area'].bind('<Return>', self.send_chat_data)
        self.window_chat.children['chat_input_area'].bind('<Shift-Return>', self.shift_enter)
        self.window_chat.window_closed(self.exit)
        self.window_chat.withdraw()

        # 创建套接字
        self.client_conn = ClientSocket()

        # 初始化消息处理函数
        self.response_handle_function = {}
        self.register(RESPONSE_LOGIN_RESULT, self.response_login_handle)
        self.register(RESPONSE_CHAT, self.response_chat_handle)

        # 初始化在线用户的用户名
        self.username = None
        # 程序正在运行的标记
        self.is_running = True

    def register(self, request_id, handle_function):
        """注册消息和消息对应的方法到字典"""
        self.response_handle_function[request_id] = handle_function

    def start_window(self):
        # 连接服务器l
        self.client_conn.connect()
        # 创建并开启子线程用来接收消息
        Thread(target=self.response_handle).start()
        # 开启窗口
        self.window.mainloop()

    def clear_input(self):
        self.window.clear_password()
        self.window.clear_username()

    def send_login_data(self,ev=None):
        """发送消息到服务器"""
        # 获取用户名密码
        username = self.window.get_login_username()
        password = self.window.get_login_password()
        # 拼接用户名密码
        request_text = RequestProtocol.request_login_result(username, password)
        # 发送给服务器
        print(request_text)
        self.client_conn.send_data(request_text)
        # print(self.client_socket.recv_data())
        # logging.debug(msg=request_text)

    def send_chat_data(self,ev=None):
        """发送聊天信息到服务器"""
        # 获取聊天框信息
        message = self.window_chat.get_inputs()
        print('message是：'+ message)
        # 拼接协议文本
        request_chat_text = RequestProtocol.request_chat(self.username, message)
        # 发送给服务器
        self.client_conn.send_data(request_chat_text)
        self.window_chat.append_message('我', message)
        # 清空输入框
        self.window_chat.clear_inputs()
        """
        在按下回车键时，不仅会触发我们绑定的方法，还会触发回车键原本的换行效果，
        但我们希望只触发绑定的方法而不进行换行，故 return ’break‘
        """
        return 'break'

    def shift_enter(self,event=None):
        """使用组合键对聊天框Text内容进行换行"""
        self.window_chat.children['chat_input_area'].insert('insert','')


    def response_handle(self):
        """不间断接收服务端消息"""
        while self.is_running:
            # 获取消息
            msg = self.client_conn.recv_data()
            print('6666666666' + msg)

            # 解析消息
            response_data = self.parse_response_data(msg)
            print(response_data)
            # 对不同的消息进行不同的响应

            handle_function = self.response_handle_function[response_data['response_id']]
            if handle_function:
                print('handle_function:')
                print(handle_function)
                handle_function(response_data)
            #
            # if response_data['response_id'] == RESPONSE_LOGIN_RESULT:
            #     self.response_login_handle(response_data)
            # elif response_data['response_id'] == RESPONSE_CHAT:
            #     self.response_chat_handle(response_data)

    @staticmethod
    def parse_response_data(message):
        """解析获取到的服务器返回信息"""
        # 使用协议约定的符号来切割消息
        response_data_list = message.split(DELIMITER)

        # 解析消息的各个组成部分
        response_data = {}

        response_data['response_id'] = response_data_list[0]

        if response_data['response_id'] == RESPONSE_LOGIN_RESULT:
            # 登录结果响应 0001|ret|username|nickname|is_running
            response_data['result'] = response_data_list[1]
            response_data['nickname'] = response_data_list[2]
            response_data['username'] = response_data_list[3]
            response_data['is_running'] = response_data_list[4]
        elif response_data['response_id'] == RESPONSE_CHAT:
            # 聊天信息响应
            response_data['nickname'] = response_data_list[1]
            response_data['message'] = response_data_list[2]

        return response_data

    def response_login_handle(self, response_data):
        """登录结果响应"""
        print('接收到登录信息')
        result = response_data['result']
        is_running = response_data['is_running']
        if result == '0':
            if is_running == '0':
                showinfo('提示', '登陆失败！账号或密码错误')
            else:
                showinfo('提示', '登陆失败！用户已在其它地方登录')
            self.clear_input()
            print('登陆失败')
            return

        # 登陆成功获取用户信息
        nickname = response_data['nickname']
        self.username = response_data['username']
        showinfo('提示', '登陆成功！')
        # 设置登录窗口标题
        self.window_chat.set_title(self.username)
        self.window_chat.update()
        # 显示聊天窗口
        self.window_chat.deiconify()
        # 隐藏登录窗口
        self.window.withdraw()

        print('登陆成功，{}的昵称为{}'.format(self.username, nickname))

    def response_chat_handle(self, response_data):
        """聊天信息响应"""
        print('接收到聊天消息', response_data)
        sender = response_data['nickname']
        message = response_data['message']
        self.window_chat.append_message(sender, message)

    def exit(self):
        """退出程序"""
        self.is_running = False
        os._exit(0)


if __name__ == '__main__':
    client = Client()
    client.start_window()
