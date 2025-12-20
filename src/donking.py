# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pytesseract
import traceback
import time
import pyautogui
import pygame
import os
import platform

# 初始化 Tesseract
def init_tesseract():
    """初始化 Tesseract OCR 引擎"""
    try:
        system_platform = platform.system()
        if system_platform == "Windows":
            pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract\tesseract.exe'
            print(f"Tesseract-OCR 路径设置成功 (平台: {system_platform})")
        elif system_platform == "Linux":
            # 在 Linux 上尝试常见路径
            possible_paths = [
                "/usr/bin/tesseract",
                "/usr/local/bin/tesseract",
                "/opt/homebrew/bin/tesseract"  # macOS Homebrew
            ]
            
            tesseract_found = False
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    print(f"Tesseract-OCR 路径设置成功: {path}")
                    tesseract_found = True
                    break
            
            if not tesseract_found:
                # 让 pytesseract 自动查找
                print("使用系统默认 Tesseract 路径")
        return True
    except Exception as e:
        print("设置 Tesseract-OCR 路径出错:", e)
        traceback.print_exc()
        return False

# 读入用户输入
screen_width = int(input("请输入屏幕宽度: (直接Enter默认1280)\n") or 1280)
screen_height = int(input("请输入屏幕高度: (直接Enter默认960)\n") or 960)

oi_width = int(27*(screen_width/1280))
oi_height = int(27*(screen_height/960))

scoreboard_width = int(21*(screen_width/1280))
scoreboard_height = int(24*(screen_height/960))

# OCR 左侧區域設置
loi_x = int(565*(screen_width/1280))
loi_y = int(10*(screen_height/960))

# OCR 右侧區域設置
roi_x = screen_width - loi_x - oi_width
roi_y = loi_y

# OCR 计分板左区域設置    
l_scoreboard_x = int(612*(screen_width/1280))
l_scoreboard_y = int(38*(screen_height/960))

# OCR 计分板右区域設置
r_scoreboard_x = screen_width - l_scoreboard_x - scoreboard_width
r_scoreboard_y = l_scoreboard_y

# 初始化音频系统
def init_audio():
    """初始化音频系统"""
    try:
        pygame.mixer.init()
        # 使用相对路径查找音乐文件
        mp3_files = [
            "donk.mp3",  # 同目录下的文件
            "src/donk.mp3",  # src目录下的文件
            r"C:\Users\Public\Music\donk.mp3"  # Windows 默认路径
        ]
        
        mp3_file = None
        for file_path in mp3_files:
            if os.path.exists(file_path):
                mp3_file = file_path
                break
                
        if mp3_file:
            pygame.mixer.music.load(mp3_file)
            print(f"音乐文件加载成功: {mp3_file}")
            return True
        else:
            print("未找到音乐文件 donk.mp3")
            return False
    except Exception as e:
        print(f"音乐系统初始化失败: {e}")
        return False

# 初始化系统
init_tesseract()
audio_available = init_audio()

side = None
sidenum = None
while side is None:
    side = input("T to start Or CT to start   __\b\b\a")
    if (side.lower() == "t" ):
        print("T start")
        sidenum = 1
    elif (side.lower() in ("ct", "c")):
        print("CT start")
        sidenum = 2
    else:
        print("Not A Valid Input, plz input again")
        side = None

number = None
number_1 = None
number_2 = None

score_num = None

# 优化参数：添加帧率控制
last_process_time = time.time()
process_interval = 0.5  # 处理间隔（秒）

# 主循環
while True:
    try:
        # 帧率控制：限制处理频率以降低CPU使用率
        current_time = time.time()
        if current_time - last_process_time < process_interval:
            time.sleep(0.05)  # 短暂休眠避免过度占用CPU
            continue
        last_process_time = current_time
        
        # 截图
        screenshot_left = pyautogui.screenshot(region=(loi_x, loi_y, oi_width, oi_height))
        screenshot_left = cv2.cvtColor(np.array(screenshot_left), cv2.COLOR_RGB2GRAY)
        screenshot_right = pyautogui.screenshot(region=(roi_x, roi_y, oi_width, oi_height))
        screenshot_right = cv2.cvtColor(np.array(screenshot_right), cv2.COLOR_RGB2GRAY)
        r_scoreboard = pyautogui.screenshot(region=(r_scoreboard_x, r_scoreboard_y, scoreboard_width, scoreboard_height))
        r_scoreboard = cv2.cvtColor(np.array(r_scoreboard), cv2.COLOR_RGB2GRAY)
        l_scoreboard = pyautogui.screenshot(region=(l_scoreboard_x, l_scoreboard_y, scoreboard_width, scoreboard_height))
        l_scoreboard = cv2.cvtColor(np.array(l_scoreboard), cv2.COLOR_RGB2GRAY)

        # 优化的预处理：简化处理步骤以提高性能
        # 使用更简单的二值化方法替代复杂的高斯模糊+OTSU阈值
        _, binary_left = cv2.threshold(screenshot_left, 180, 255, cv2.THRESH_BINARY_INV)
        _, binary_right = cv2.threshold(screenshot_right, 180, 255, cv2.THRESH_BINARY_INV)
        _, binary_left_scoreboard = cv2.threshold(l_scoreboard, 180, 255, cv2.THRESH_BINARY_INV)
        _, binary_right_scoreboard = cv2.threshold(r_scoreboard, 180, 255, cv2.THRESH_BINARY_INV)
        
        # 适度的膨胀处理
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated_left = cv2.dilate(binary_left, kernel, iterations=1)
        dilated_right = cv2.dilate(binary_right, kernel, iterations=1)
        dilated_left_scoreboard = cv2.dilate(binary_left_scoreboard, kernel, iterations=1)
        dilated_right_scoreboard = cv2.dilate(binary_right_scoreboard, kernel, iterations=1)

        # OCR
        config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
        text_left = pytesseract.image_to_string(dilated_left, config=config)
        print("左侧区域识别结果:", repr(text_left))
        text_right = pytesseract.image_to_string(dilated_right, config=config)
        print("右侧区域识别结果:", repr(text_right))
        text_left_scoreboard = pytesseract.image_to_string(dilated_left_scoreboard, config=config)
        print("计分板区域识别结果:", repr(text_left_scoreboard))
        text_right_scoreboard = pytesseract.image_to_string(dilated_right_scoreboard, config=config)
        print("计分板区域识别结果:", repr(text_right_scoreboard))

        try:
            left_scoreboard_number = int(text_left_scoreboard.strip())
            right_scoreboard_number = int(text_right_scoreboard.strip())

            print("左侧计分板数字 =", left_scoreboard_number)
            print("右侧计分板数字 =", right_scoreboard_number)

            if sidenum == 1: #T
                number_1 = int(text_right.strip())
                number_2 = int(text_left.strip())
            elif sidenum == 2: #CT
                number_1 = int(text_left.strip())
                number_2 = int(text_right.strip())

            # 设置Number
            if left_scoreboard_number + right_scoreboard_number <= 12:
                score_num = 1
            elif left_scoreboard_number + right_scoreboard_number > 12:
                score_num = 2

            if score_num == 1:
                number = number_1
            elif score_num == 2:
                number = number_2

            print("当前识别到己方场上人数 =", number)

            # 只有在音频可用时才尝试播放/停止音乐
            if audio_available:
                if number == 1:
                    if not pygame.mixer.music.get_busy():
                        print("▶ 播放音乐")
                        pygame.mixer.music.play(-1)  # 循环播放
                elif number == 5:
                    if pygame.mixer.music.get_busy():
                        print("■ 停止音乐")
                        pygame.mixer.music.stop()

        except ValueError:
            print("未识别到有效数字")

    except Exception as e:
        print("程序出错:", e)
        traceback.print_exc()

cv2.destroyAllWindows()