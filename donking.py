# -*- coding: utf-8 -*-
from re import L
import cv2
import numpy as np
import pytesseract
import traceback
import time
import pyautogui
import pygame

# 初始化 Tesseract
try:
    pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract\tesseract.exe'
    print("Tesseract-OCR 路径设置成功")
except Exception as e:
    print("设置 Tesseract-OCR 路径出错:", e)
    traceback.print_exc()

# OCR 左侧區域設置
loi_x = 565
loi_y = 10
loi_width = 27
loi_height = 27

# OCR 右侧區域設置
roi_x = 665
roi_y = 10
roi_width = 27
roi_height = 27

# OCR 计分板区域設置    
l_scoreboard_x = 615
l_scoreboard_y = 10
l_scoreboard_width = 27
l_scoreboard_height = 27

r_scoreboard_x = 625
r_scoreboard_y = 10
r_scoreboard_width = 27
r_scoreboard_height = 27

# 初始化
pygame.mixer.init()
MP3_FILE = r"C:\Users\Public\Music\donk.mp3"
pygame.mixer.music.load(MP3_FILE)

# 主循環
while True:
    try:
        # 截图
        screenshot_left = pyautogui.screenshot(region=(loi_x, loi_y, loi_width, loi_height))
        screenshot_left = cv2.cvtColor(np.array(screenshot_left), cv2.COLOR_RGB2GRAY)
        screenshot_right = pyautogui.screenshot(region=(roi_x, roi_y, roi_width, roi_height))
        screenshot_right = cv2.cvtColor(np.array(screenshot_right), cv2.COLOR_RGB2GRAY)
        r_scoreboard = pyautogui.screenshot(region=(r_scoreboard_x, r_scoreboard_y, r_scoreboard_width, r_scoreboard_height))
        r_scoreboard = cv2.cvtColor(np.array(r_scoreboard), cv2.COLOR_RGB2GRAY)
        l_scoreboard = pyautogui.screenshot(region=(l_scoreboard_x, l_scoreboard_y, l_scoreboard_width, l_scoreboard_height))
        l_scoreboard = cv2.cvtColor(np.array(l_scoreboard), cv2.COLOR_RGB2GRAY)

        # 预处理
        blurred_left = cv2.GaussianBlur(screenshot_left, (5, 5), 0)
        _, binary_left = cv2.threshold(blurred_left, 128, 255,
                                  cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        blurred_right = cv2.GaussianBlur(screenshot_right, (5, 5), 0)
        _, binary_right = cv2.threshold(blurred_right, 128, 255,
                                  cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        blurred_left_scoreboard = cv2.GaussianBlur(l_scoreboard, (5, 5), 0)
        _, binary_left_scoreboard = cv2.threshold(blurred_left_scoreboard, 128, 255,
                                  cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        blurred_right_scoreboard = cv2.GaussianBlur(r_scoreboard, (5, 5), 0)
        _, binary_right_scoreboard = cv2.threshold(blurred_right_scoreboard, 128, 255,
                                  cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
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

            if left_scoreboard_number + right_scoreboard_number  == 0:
                side = input("T to start Or CT to start")
                if side == "T":
                    print("T start")
                    number_1 = int(text_left.strip())
                    number_2 = int(text_right.strip())
                elif side == "CT":
                    print("CT start")
                    number1 = int(text_right.strip())
                    number2 = int(text_left.strip())

            if left_scoreboard_number + right_scoreboard_number <= 12:
                print("识别数字 =", number_1)
                number = number_1
            elif left_scoreboard_number + right_scoreboard_number > 12:
                print("识别数字 =", number_2)
                number = number_2

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

        time.sleep(0.5)

    except Exception as e:
        print("程序出错:", e)
        traceback.print_exc()

cv2.destroyAllWindows()