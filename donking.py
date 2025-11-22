# -*- coding: utf-8 -*-
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

# OCR 區域設置
roi_x = 565
roi_y = 10
roi_width = 27
roi_height = 27

# 初始化
pygame.mixer.init()
MP3_FILE = r"C:\Users\Public\Music\donk.mp3"
pygame.mixer.music.load(MP3_FILE)

# 主循環
while True:
    try:
        # 截图
        screenshot = pyautogui.screenshot(region=(roi_x, roi_y, roi_width, roi_height))
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        # 预处理
        blurred = cv2.GaussianBlur(screenshot, (5, 5), 0)
        _, binary = cv2.threshold(blurred, 128, 255,
                                  cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated = cv2.dilate(binary, kernel, iterations=1)

        # OCR
        config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(dilated, config=config)
        print("识别结果:", repr(text))

        try:
            number = int(text.strip())
            print("识别数字 =", number)

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