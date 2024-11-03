import serial
import time

# 配置串行通信的端口和波特率
# 请确保端口名与你的系统上显示的Arduino端口一致
port = 'COM3'  # 对于Windows，通常是COMx
baud_rate = 9600

# 打开串口
ser = serial.Serial(port, baud_rate, timeout=1)

# 等待Arduino初始化
time.sleep(2)

try:
    while True:
        # 发送字符'H'到Arduino来打开LED
        ser.write(b'H')
        print("Sent 'H' to Arduino")
        time.sleep(1)

        # 发送字符'L'到Arduino来关闭LED
        ser.write(b'L')
        print("Sent 'L' to Arduino")
        time.sleep(1)

except KeyboardInterrupt:
    # 如果按下Ctrl+C，则关闭串口
    ser.close()
