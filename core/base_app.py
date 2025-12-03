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


class AppAutoManager:

    def appium_init(self):
        print("⚙️ 正在初始化Appium驱动...")
        max_retries = 3
        for attempt in range(max_retries):
            try:
                caps = UiAutomator2Options()
                caps.set_capability("appium:deviceName", "127.0.0.1:7555")
                caps.set_capability("appium:appPackage", "com.wxbz_sgshjz.ks10")
                caps.set_capability("appium:appActivity", ".MainActivity")
                caps.set_capability("appium:automationName", "UiAutomator2")
                caps.set_capability("appium:noReset", True)
                caps.set_capability("appium:newCommandTimeout", 1200)  # 新增20分钟超时设置
                caps.set_capability("appium:udid", "127.0.0.1:7555")  # 明确指定UDID
                caps.set_capability("appium:ensureWebviewsHavePages", True)
                caps.set_capability("appium:nativeWebScreenshot", True)
            
                appium_server_url = "http://127.0.0.1:4723"
                try:
                    driver = webdriver.Remote(appium_server_url, options=caps)
                    driver.implicitly_wait(15)
                    print(f"✅ Appium驱动初始化成功 - 服务器: {appium_server_url}")
                    return driver
                except Exception as e:
                    if attempt == max_retries - 1:
                        print(f"❌ Appium连接失败(尝试{max_retries}次): {str(e)}")
                        raise
                    print(f"⚠️ 连接失败，第{attempt+1}次重试...")
                    time.sleep(5)
            except Exception as e:
                print(f"❌ Appium连接失败: {str(e)}")
                raise

    def quit(self, driver):
        if driver:
            try:
                driver.quit()
                print("\n🛑 驱动已关闭")
            except Exception as e:
                print(f"\n⚠️ 关闭驱动时出错: {str(e)}")


app = AppAutoManager()
app.appium_init()