import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import subprocess
import threading
import queue

# 全局队列用于存储子进程的输出
output_queue = queue.Queue()


# 处理子进程输出的函数
def read_output(proc, queue):
    for line in proc.stdout:
        decoded_line = line.decode('utf-8').strip()
        queue.put(decoded_line)
    proc.stdout.close()


# 更新Text组件的函数
def update_text():
    try:
        while True:
            line = output_queue.get_nowait()
            text_widget.insert(tk.END, line + "\n")
            text_widget.see(tk.END)  # 自动滚动到文本末尾
    except queue.Empty:
        root.after(100, update_text)  # 如果没有数据，则稍后重试


# 打开并运行指定Python脚本的函数
def open_program(script_name):
    if script_name == "damoxing.py":
        proc = subprocess.Popen(["python", script_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        threading.Thread(target=read_output, args=(proc, output_queue)).start()
        update_text()  # 只对damoxing.py启用输出更新
    else:
        subprocess.Popen(["python", script_name])  # 其他脚本直接运行，不捕获输出


# 创建主窗口
root = tk.Tk()
root.title("Program Launcher")
root.geometry("400x500")  # 设置窗口大小

# 使用Ttk风格
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding="5 10")

# 创建Frame用于组织按钮
button_frame = ttk.Frame(root, padding="10 10 10 10")
button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 创建按钮并放置到Frame上，不使用图标
button1 = ttk.Button(button_frame, text="串口通信", command=lambda: open_program("qhzy.py"))
button1.grid(row=0, column=0, pady=10, padx=10)

button2 = ttk.Button(button_frame, text="拍照功能", command=lambda: open_program("paizhao.py"))
button2.grid(row=1, column=0, pady=10, padx=10)

button3 = ttk.Button(button_frame, text="大模型计算", command=lambda: open_program("damoxing.py"))
button3.grid(row=2, column=0, pady=10, padx=10)

# 创建一个分隔符
separator = ttk.Separator(root, orient="horizontal")
separator.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)

# 创建Text组件用于显示damoxing.py的输出（如果需要的话，可以调整大小和位置）
text_widget = scrolledtext.ScrolledText(root, height=10, width=40, wrap=tk.WORD, font=("Helvetica", 10))
text_widget.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=10)

# 调整按钮Frame的列配置，使其居中（如果需要的话）
button_frame.grid_columnconfigure(0, weight=1)

# 启动事件循环
root.mainloop()