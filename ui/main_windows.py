import tkinter as tk
class Ui_MainWindows():
    def __init__(self,ui):
        root = ui
        self.setupUi(root)
    def setupUi(self,myui):
        myui.title("MyApp") # 修改框体的名字,也可在创建时使用className参数来命名；
        width = 1100
        height = 800
        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        screenwidth = myui.winfo_screenwidth()
        screenheight = myui.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        myui.geometry(alignstr)
        # 设置窗口是否可变长、宽，True：可变，False：不可变
        myui.resizable(width=True, height=True)
        # 定义一个容器放接受区域的显示
        self.frame_revaera = tk.Frame(myui, bg="#FFFFF0") #象牙色
        self.frame_revaera.place(relx = 0.02, rely = 0.02, relheight = 0.58, relwidth = 0.96)
        self.label_rev = tk.Label(self.frame_revaera, text = "接收区域")
        self.label_rev.place(relx = 0.02, rely = 0.02, relheight = 0.03, relwidth = 0.05)
        self.text_rev = tk.Text(self.frame_revaera, state = tk.DISABLED)
        self.text_rev.place(relx = 0.02, rely = 0.06, relheight = 0.92, relwidth = 0.96)

        # 创建滚动条
        scroll = tk.Scrollbar(self.frame_revaera)
        #side放到窗体的那一侧   fill填充
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        #关联
        scroll.config(command=self.text_rev.yview)
        self.text_rev.config(yscrollcommand=scroll.set)

        # 定义一个容器放发送区域的显示
        self.frame_sendaera = tk.Frame(myui, bg="#FFFFF0") #象牙色
        self.frame_sendaera.place(relx = 0.02,rely = 0.62,relheight = 0.36, relwidth = 0.96)
        self.label_send = tk.Label(self.frame_sendaera, text = "发送区域")
        self.label_send.place(relx = 0.02, rely = 0.02, relheight = 0.05, relwidth = 0.05)



        # 增加按钮


    def print_inrevarea(self,printstr):
        self.text_rev.config(state = tk.NORMAL) #由于之前把这个框DISALBE 所以写之前需要打开
        self.text_rev.insert(tk.END,printstr)
        self.text_rev.config(state = tk.DISABLED) #再次关闭
        # 刷新显示在最后一页
        self.text_rev.see(tk.END)
        # self.text_rev.update()


def test():
    root = tk.Tk()
    ui = Ui_MainWindows(root)
    root.mainloop()

if __name__ == '__main__':
    test()
    # test_connect()