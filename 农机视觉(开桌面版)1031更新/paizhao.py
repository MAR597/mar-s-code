import cv2
import os

# 创建VideoCapture对象，使用RTSP流地址
cap = cv2.VideoCapture("rtsp://admin:12345@192.168.7.107/your_stream")

# 检查视频是否成功打开
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# 设置窗口名称
window_name = 'RTSP Stream'
cv2.namedWindow(window_name)

# 用于保存照片的变量
photo_taken = False
photo_path = "captured_photo.jpg"

# 循环读取视频帧
while True:
    # 读取一帧
    ret, frame = cap.read()

    # 如果帧读取失败，则退出循环
    if not ret:
        print("Error: Could not read frame.")
        break

        # 显示帧
    cv2.imshow(window_name, frame)

    # 检测按键输入
    key = cv2.waitKey(1) & 0xFF

    # 如果按下'c'键，则拍摄照片
    if key == ord('c'):
        cv2.imwrite(photo_path, frame)
        print(f"Photo captured and saved to {photo_path}")
        photo_taken = True

        # 如果按下'q'键，则退出循环
    elif key == ord('q'):
        break

    # 释放VideoCapture对象
cap.release()

# 销毁所有OpenCV窗口
cv2.destroyAllWindows()

# 检查是否拍摄了照片，并在退出后处理它
if photo_taken:
    def process_photo(file_path):
        # 这里添加处理照片的代码
        # 例如，使用OpenCV加载图像并进行某些操作
        image = cv2.imread(file_path)
        # ... 进行图像处理 ...
        # 注意：这里的代码只是示例，并没有实际的处理逻辑
        print("Photo processing function called.")
        # 如果需要，可以在这里保存处理后的图像
        # cv2.imwrite('processed_photo.jpg', processed_image)


    process_photo(photo_path)
else:
    print("No photo taken.")