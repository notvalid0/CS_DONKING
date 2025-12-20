# 关于此项目的说明文档

## About

本人非CS玩家，室友偶然提供灵感后完成此项目，问题颇多；

实现流程十分简单：截图 -> 识图 -> 辨别数字 -> 播放音乐

欢迎提交Issue

**基于Tesseract-OCR开发**

### How To Use?

1. 下载并安装[tesseract-ocr_w64-setup](https://github.com/UB-Mannheim/tesseract/wiki)文件，安装tesseract在E:/Tesseract文件夹[*]下

2. 复制donk.mp3在C:\Public\Music目录[*]下

3. 双击运行已用`pyinstaller`构建好的binary文件(CS2_DONKING.exe)[如果是CSGO用户请下载CSGO_DONKING.exe]

4. 修改CS的游戏设置-HUD设置，显示存活人数

5. 修改CS的分辨率为全屏-`1280*960` [*] (V2.2新增: 现已不需要)

## Note (对于V1.0):

***对于有PYTHON环境或者有特殊需求的用户，可以自行修改代码后用pyinstaller打包或直接运行***

1. Tesseract文件夹目录可以修改，在donking.py第12行。

2. Mp3文件目录可以修改，在donking.py第26行

3. OCR截图区域是基于这个分辨率，可以在line19-line22修改代码[电脑区域坐标为左上角(0,0)]，建议使用微信截图获取区域左上角坐标位置与区域大小

4. 如需打包，可以`pip install pyinstaller` 后使用`pyinstaller--onefile xxx.py` 构建EXE文件 

> ***自行打包需保证电脑有numpy, opencv-python, pytesseract库***


## CHANGELOG

### Version 2.2 
  2025/12/20
  优化用户读入&&音乐检测健壮性，提高standalone文件使用简便性

### Version 2.1
  2025/21/19
  优化系统界面大小设置，合并相似代码减少代码设置量

### Version 2.0 (Nightly)
  2025/12/16
  优化程序逻辑，开局选择出生边。
