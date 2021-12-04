import socket
from config import *


class ServerSocket(socket.socket):
    def __init__(self):
        """初始化socket"""
        # 在子类中调用父类的构造函数是为了让子类既有父类的属性又有子类自己的属性
        # 设置为TCP类型
        # soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super(ServerSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)

        # 绑定ip和端口号
        self.bind((SERVER_IP, SERVER_PORT))

        # 设置为监听模式,最大允许128个连接
        self.listen(128)
