import tkinter as tk
import serial
import serial.tools.list_ports

class SerialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("串口通信示例")
        self.serial_port = None
        self.serial_open = False
        self.pressed_buttons = set()
        self.command_map = {
            'A': '前进', 'B': '后退', 'D': '左转', 'C': '右转', 'E': '停止'
        }
        self.root.option_add('*Font', ('Arial', 20))
        self.configure_serial()
        self.create_buttons()

    def configure_serial(self):
        ports = serial.tools.list_ports.comports()
        port_names = [port.device for port in ports if 'USB' in port.description]
        if not port_names:
            print("没有找到可用的串口")
            return
        try:
            self.serial_port = serial.Serial(port_names[0], 9600, timeout=1)
            if self.serial_port.is_open:
                self.serial_open = True
                print(f"已打开串口: {self.serial_port.port}")
        except serial.SerialException as e:
            print(f"无法打开串口: {e}")

    def create_buttons(self):
        # 创建按钮
        btn_forward = tk.Button(self.root, text='前进', width=10, height=3)
        btn_forward.grid(row=0, column=1, padx=10, pady=10)
        btn_forward.bind("<ButtonPress>", lambda event: self.start_sending('A'))
        btn_forward.bind("<ButtonRelease>", lambda event: self.stop_sending('A'))

        btn_backward = tk.Button(self.root, text='后退', width=10, height=3)
        btn_backward.grid(row=2, column=1, padx=10, pady=10)
        btn_backward.bind("<ButtonPress>", lambda event: self.start_sending('B'))
        btn_backward.bind("<ButtonRelease>", lambda event: self.stop_sending('B'))

        btn_left = tk.Button(self.root, text='左转', width=10, height=3)
        btn_left.grid(row=1, column=0, padx=10, pady=10)
        btn_left.bind("<ButtonPress>", lambda event: self.start_sending('D'))
        btn_left.bind("<ButtonRelease>", lambda event: self.stop_sending('D'))

        btn_right = tk.Button(self.root, text='右转', width=10, height=3)
        btn_right.grid(row=1, column=2, padx=10, pady=10)
        btn_right.bind("<ButtonPress>", lambda event: self.start_sending('C'))
        btn_right.bind("<ButtonRelease>", lambda event: self.stop_sending('C'))

        btn_stop = tk.Button(self.root, text='停止', width=10, height=3)
        btn_stop.grid(row=3, column=1, padx=10, pady=10)
        btn_stop.bind("<ButtonPress>", lambda event: self.start_sending('E'))
        btn_stop.bind("<ButtonRelease>", lambda event: self.stop_sending('E'))

        btn_exit = tk.Button(self.root, text='退出', width=10, height=3, command=self.close_app)
        btn_exit.grid(row=4, column=1, padx=10, pady=10)

    def start_sending(self, char):
        if self.serial_open and self.serial_port:
            self.pressed_buttons.add(char)
            self.serial_port_write(char)

    def stop_sending(self, char):
        if char in self.pressed_buttons:
            self.pressed_buttons.remove(char)
            if not self.pressed_buttons:
                self.serial_port_write('E')

    def serial_port_write(self, char):
        if self.serial_open and self.serial_port:
            self.serial_port.write(char.encode())
            print(f"已发送字符: {char}")

    def close_app(self):
        self.stop_sending('dummy')
        self.close_serial()
        self.root.destroy()

    def close_serial(self):
        if self.serial_open and self.serial_port:
            self.serial_port.close()
            self.serial_open = False
            print(f"已关闭串口: {self.serial_port.port}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('300x400')
    app = SerialApp(root)
    root.mainloop()
