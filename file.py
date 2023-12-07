import configparser
import logging

import cv2
import pygame


class file:
    def __init__(self, filename):
        self.filename = filename

    def log(self):  # 日志文件
        logger = logging.getLogger()  # 实例化日志对象
        hdlr = logging.FileHandler(self.filename)  # 确认日志文件
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')  # 格式化  日期,级别,信息
        hdlr.setFormatter(formatter)  # 将格式设置到处理器上
        logger.addHandler(hdlr)  # 将处理器加到日志对象里
        logger.setLevel(logging.NOTSET)  # 设置信息输出级别

    def cof(self):  # 配置文件
        config = configparser.ConfigParser()  # 实例化配置文件对象
        config.read(self.filename)  # 读取配置文件
        APP_ID = config['baidu_aip']['APP_ID']
        API_KEY = config['baidu_aip']['API_KEY']
        SECRET_KEY = config['baidu_aip']['SECRET_KEY']
        return APP_ID, API_KEY, SECRET_KEY

    def get_file_content(self):  # 读取图片
        with open(self.filename, 'rb') as f:
            return f.read()

    def readwrite(self, cap):  # 读写每一帧图片
        sucess, frame = cap.read()  # 读取    一帧图片
        cv2.imwrite(self.filename, frame)  # 将图片写入filename
        img = pygame.image.load(self.filename)  # 读取图片
        return img
