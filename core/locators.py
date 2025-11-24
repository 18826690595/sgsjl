import time
from time import sleep
import os  # 添加这行导入语句
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import cv2
import numpy as np
import pytesseract
from PIL import Image


class Locators:
    def __init__(self, driver=None):
        self.driver = driver

    pass


# 修改测试部分
if __name__ == "__main__":
    # 这里应该使用实际的 driver 对象，例如:
    # from appium import webdriver
    # driver = webdriver.Remote(...)
    # test = Tap_By_Login(driver)

    # 临时模拟测试
    class MockDriver:
        def get_window_size(self):
            return {'width': 1080, 'height': 1920}


    test = Locators()
    test.get_snapshot("test_username")
