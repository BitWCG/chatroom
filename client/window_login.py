from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import Frame
from tkinter import Button, LEFT, END
import logging

# logging.basicConfig(filename='my.log',level=logging.DEBUG)


class WindowLogin(Tk):

    def __init__(self):
        """初始化登录窗口"""
        super(WindowLogin, self).__init__()
        # 设置窗口属性
        self.window_init()
        logging.debug("This is a debug log.")
        # 填充控件
        self.add_widgets()
        # 设置窗口图标
        self.iconbitmap('./resources/qq.ico')

        # self.login_button_click(lambda : print(self.clear_username()))
        # self.reset_button_click([self.clear_username,self.clear_password()])

    def window_init(self):
        """初始化窗口属性"""
        self.title('开黑聊天软件')
        # 设置窗口不能被拉伸
        self.resizable(False, False)
        # 登录窗口大小
        window_width = 300
        window_height = 150

        # 窗口位置
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        pos_x = (screen_width - window_width) / 2
        pos_y = (screen_height - window_height) / 2

        self.geometry('{}x{}+{}+{}'.format(window_width, window_height, int(pos_x), int(pos_y)))

    def add_widgets(self):
        """添加控件到窗口中"""

        # 用户名--标签
        username_label = Label(self, name='username_label')
        username_label['text'] = ' 用户名: '
        username_label.grid(row=0, column=0, padx=10, pady=10)
        # 用户名--文本框
        username_entry = Entry(self, name='username_entry')
        username_entry['width'] = 23
        username_entry.grid(row=0, column=1)

        # 密码--标签
        password_label = Label(self, name='password_label')
        password_label['text'] = ' 密    码: '
        password_label.grid(row=1, column=0)

        # 密码--文本框
        password_entry = Entry(self, name='password_entry')
        password_entry['width'] = 23
        password_entry['show'] = '*'
        password_entry.grid(row=1, column=1)

        # Frame容器（类似于前端的div）
        button_frame = Frame(self, name='button_frame')

        # 重置按钮
        reset_button = Button(button_frame, name='reset_button')
        reset_button['text'] = ' 重置 '
        reset_button['relief'] = 'groove'
        reset_button.pack(side=LEFT, pady=10, padx=20)
        # 登录按钮
        login_button = Button(button_frame, name='login_button')
        login_button['text'] = ' 登录 '
        login_button['relief'] = 'groove'
        login_button.pack(side=LEFT)

        button_frame.grid(row=2, columnspan=2, pady=5)
        # print(self.children['button_frame'].children)

    def reset_button_click(self, command):
        reset_button = self.children['button_frame'].children['reset_button']
        reset_button['command'] = command

    def login_button_click(self, command):
        login_button = self.children['button_frame'].children['login_button']
        login_button['command'] = command

    def window_close(self, command):
        """关闭窗口的响应注册"""
        self.protocol('WM_DELETE_WINDOW', command)

    def get_login_username(self):
        """获取登录用户名"""
        return self.children['username_entry'].get()

    def get_login_password(self):
        """获取登录密码"""
        return self.children['password_entry'].get()

    def clear_username(self):
        """清除用户名"""
        self.children['username_entry'].delete(0,END)

    def clear_password(self):
        """清除登录密码"""
        self.children['password_entry'].delete(0,END)


if __name__ == '__main__':
    window = WindowLogin()
    window.mainloop()
