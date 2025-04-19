import cv2
import time

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 晴天和阴天图片计数器
clear_count = 0
foggy_count = 0

# 保存路径
save_path = "./images/"

while True:
    # 读取一帧画面
    ret, frame = cap.read()

    if not ret:
        print("无法获取画面")
        break

    # 每5秒保存一次画面
    time.sleep(5)

    # 检查是否已经保存了50张晴天和50张阴天图片
    if clear_count < 50:
        # 生成晴天图片文件名
        clear_filename = f"{save_path}clear_{str(clear_count + 1).zfill(3)}.png"
        # 保存晴天图片
        cv2.imwrite(clear_filename, frame)
        print(f"已保存晴天图片: {clear_filename}")
        clear_count += 1
    elif foggy_count < 50:
        # 生成阴天图片文件名
        foggy_filename = f"{save_path}foggy_{str(foggy_count + 1).zfill(3)}.png"
        # 保存阴天图片
        cv2.imwrite(foggy_filename, frame)
        print(f"已保存阴天图片: {foggy_filename}")
        foggy_count += 1
    else:
        # 已经保存了足够的图片，退出循环
        break

# 释放摄像头并关闭所有窗口
cap.release()
cv2.destroyAllWindows()
    