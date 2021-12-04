import socket
from config import *


class ClientSocket(socket.socket):
    """客户端套接字的自定义处理"""
    def __init__(self):
        # 设置为TCP套接字
        super(ClientSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """自动连接到服务器"""
        super(ClientSocket, self).connect((SERVER_IP, SERVER_PORT))

    def recv_data(self):
        """接收数据并解码"""
        return self.recv(512).decode('utf-8')

    def send_data(self, message):
        """发送数据"""
        return self.send(message.encode('utf-8'))

    def close(self):
        """关闭套接字"""
        self.close()

# if __name__ == '__main__':
#     client = ClientSocket()
#     client.connect()
#     msg = '1651651'
#     client.send_data(msg)
#     print(client.recv_data())