# 模拟客户端连接服务器

import socket


def test():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(('127.0.0.1', 10095))
    while True:
        msg = input('请输入：')
        soc.send(msg.encode('utf-8'))
        recv_data = soc.recv(512)
        print(recv_data.decode('utf-8'))
    soc.close()


if __name__ == '__main__':
    test()
