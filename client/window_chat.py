from tkinter import Toplevel, NORMAL
from tkinter.scrolledtext import ScrolledText
from tkinter import Text
from tkinter import Button
from tkinter import END
from tkinter import UNITS
from tkinter import DISABLED
from time import time, strftime, localtime


class WindowChat(Toplevel):

    def __init__(self):
        super(WindowChat, self).__init__()

        # 设置顶层窗口大小和位置
        self.geometry('{}x{}+{}+{}'.format(795, 505,int(self.location()[0]),int(self.location()[1])))

        # 设置窗口为不可拉伸
        self.resizable(False, False)

        # 为顶层窗口添加组件
        self.add_widget()

        # 设置窗口图标
        self.iconbitmap('./resources/qq.ico')

        # self.send_button_click(lambda :self.append_message('郭昊东', '我是傻逼'))

    def location(self):
        win_width = 795
        win_height = 505
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        return (screen_width - win_width) / 2, (screen_height - win_height) / 2

    def add_widget(self):
        """添加窗口内的组件"""

        # 滚动式显示消息的聊天窗口
        chat_text_area = ScrolledText(self)
        chat_text_area['width'] = 85
        chat_text_area['height'] = 20
        chat_text_area.grid(row=0, column=0, columnspan=2)
        chat_text_area.tag_config('green', foreground='#008B00')
        chat_text_area.tag_config('system', foreground='red')
        chat_text_area['state'] = DISABLED
        # 用添加键值对的方式将聊天窗口添加到顶层窗口中，方便之后的查找
        self.children['chat_text_area'] = chat_text_area

        # 输入框
        chat_input_area = Text(self, name='chat_input_area')
        chat_input_area['width'] = 70
        chat_input_area['height'] = 7
        chat_input_area.grid(row=1, column=0, pady=10)
        # chat_input_area.bind('<Return>', self.entry_button)

        # 发送按钮
        send_button = Button(self, name='send_button')
        send_button['text'] = '发送'
        send_button['width'] = 10
        send_button['height'] = 5
        send_button.grid(row=1, column=1)

    # def entry_button(self,ev=None):
    #     print(self.get_inputs())

    def set_title(self, title):
        """设置聊天室窗口标题"""
        self.title('欢迎{}进入聊天室'.format(title))

    def send_button_click(self, command):
        """注册事件，当发送按钮被点击时执行 command 方法"""
        self.children['send_button']['command'] = command

    def get_inputs(self):
        """获取输入框内容"""
        text = self.children['chat_input_area'].get(0.0, END)
        # text = text.replace('\n','')
        return text

    def clear_inputs(self):
        """清空输入框内容"""
        return self.children['chat_input_area'].delete(1.0, END)

    def append_message(self, sender, message):
        """添加一条消息到聊天区"""
        send_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        sender_info = '{} : {}\n'.format(sender, send_time)
        # 将聊天区设置为可以输入（insert）
        self.children['chat_text_area']['state'] = NORMAL
        self.children['chat_text_area'].insert(END, sender_info, 'green')
        self.children['chat_text_area'].insert(END, ' ' + message)
        # 将聊天区设置为不可输入
        self.children['chat_text_area']['state'] = DISABLED
        # 向下滚动屏幕
        self.children['chat_text_area'].yview_scroll(3, UNITS)

    def window_closed(self, command):
        """注册关闭窗口时执行的命令"""
        self.protocol('WM_DELETE_WINDOW', command)


if __name__ == '__main__':
    WindowChat().mainloop()
