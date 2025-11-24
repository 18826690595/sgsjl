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
    def __init__(self, device_id="127.0.0.1:7555", package_name="com.wxbz_sgshjz.ks10"):
        self.device_id = device_id
        self.package_name = package_name
        self.driver = None
        # 检查Tesseract OCR是否可用
        try:
            # 测试中文OCR是否可用
            pytesseract.image_to_string(Image.new('RGB', (100, 100)), lang='chi_sim')
            print("✅ Tesseract OCR 中文识别已正确配置")
            pytesseract.get_tesseract_version()
            print("✅ Tesseract OCR 已正确安装并配置")
        except EnvironmentError as e:
            print(f"⚠️ 警告: Tesseract OCR配置错误 - {str(e)}")
            print("请确保:")
            print("1. 已从 https://github.com/UB-Mannheim/tesseract/wiki 下载并安装Tesseract OCR")
            print("2. 已下载语言数据文件(如eng.traineddata)并放在C:\\Program Files\\Tesseract-OCR\\tessdata目录下")
        except EnvironmentError:
            print("⚠️ 警告: Tesseract OCR未安装或不在PATH中，文字识别功能将不可用")
            print("请从 https://github.com/UB-Mannheim/tesseract/wiki 下载并安装Tesseract OCR")
        # 图像识别阈值
        # 设置Desired Capabilities
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "emulator-5554",
            "appPackage": "com.example.game",
            "appActivity": ".MainActivity",
            "automationName": "UiAutomator2"
        }
        # 初始化Appium驱动
        print(f"🚀 初始化自动化管理器 - 设备ID: {device_id}, 包名: {package_name}")
        self.appium_init()

    def appium_init(self):
        print("⚙️ 正在初始化Appium驱动...")
        caps = UiAutomator2Options()
        caps.set_capability("appium:deviceName", self.device_id)
        caps.set_capability("appium:appPackage", self.package_name)
        caps.set_capability("appium:appActivity", ".MainActivity")
        caps.set_capability("appium:automationName", "UiAutomator2")
        caps.set_capability("appium:noReset", True)

        appium_server_url = "http://127.0.0.1:4723"
        try:
            self.driver = webdriver.Remote(appium_server_url, options=caps)
            self.driver.implicitly_wait(15)
            print(f"✅ Appium驱动初始化成功 - 服务器: {appium_server_url}")
        except Exception as e:
            print(f"❌ Appium连接失败: {str(e)}")
            raise

    def find_game_entry(self, image_path=None, button_name=None, duration=300):
        best_match = None
        # 如果未提供image_path，则获取当前屏幕截图
        if image_path is None:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_np = np.frombuffer(screenshot, np.uint8)
            screen = cv2.imdecode(screenshot_np, cv2.IMREAD_COLOR)
            image = screen
        else:
            # 读取提供的图片
            image = cv2.imread(image_path)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 图像预处理优化
        # 1. 二值化
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 2. 降噪优化
        kernel = np.ones((1, 1), np.uint8)  # 减小核大小避免过度腐蚀
        processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        # 3. 锐化优化
        processed = cv2.filter2D(processed, -1, np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]))

        # 使用pytesseract获取文字位置信息 - 配置优化
        config = '--psm 6 --oem 3 -c preserve_interword_spaces=1 -l chi_sim'  # 添加简体中文支持
        data = pytesseract.image_to_data(
            processed,
            lang='chi_sim+eng',  # 添加英文支持
            output_type=pytesseract.Output.DICT,
            config=config
        )

        # 查找文字位置
        target_text = button_name
        target_chars = list(target_text)  # 拆分为单个字符
        found_chars = []
        tolerance = 5  # y坐标容差范围

        # 第一次遍历：收集所有匹配字符
        for i, text in enumerate(data['text']):
            text = text.strip()
            if text in target_chars:  # 检查是否是目标字符之一
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                found_chars.append({
                    'char': text,
                    'x': x,
                    'y': y,
                    'w': w,
                    'h': h
                })

        # 第二次遍历：找出包含所有目标字符的组
        if len(found_chars) >= len(target_chars):
            # 按y坐标分组
            y_groups = {}
            for char in found_chars:
                y_key = None
                for y_val in y_groups:
                    if abs(y_val - char['y']) <= tolerance:
                        y_key = y_val
                        break
                if y_key is None:
                    y_key = char['y']
                if y_key not in y_groups:
                    y_groups[y_key] = []
                y_groups[y_key].append(char)

            # 改进：找出包含所有目标字符且顺序正确的组
            best_match = None
            best_score = 0
            for y_val, chars in y_groups.items():
                # 按x坐标排序
                sorted_chars = sorted(chars, key=lambda c: c['x'])

                # 检查是否包含所有目标字符且顺序正确
                char_sequence = [c['char'] for c in sorted_chars]
                matched = True
                score = 0

                # 检查字符顺序和间距
                for i in range(len(char_sequence) - len(target_chars) + 1):
                    if ''.join(char_sequence[i:i + len(target_chars)]) == target_text:
                        # 计算字符间距一致性得分
                        spacing_consistent = True
                        for j in range(1, len(target_chars)):
                            prev_char = sorted_chars[i + j - 1]
                            curr_char = sorted_chars[i + j]
                            if abs((curr_char['x'] - prev_char['x'] - prev_char['w']) -
                                   (sorted_chars[i + 1]['x'] - sorted_chars[i]['x'] - sorted_chars[i]['w'])) > 5:
                                spacing_consistent = False
                                break

                        if spacing_consistent:
                            score = len(target_chars)  # 基础分
                            # 额外加分项：周围没有干扰字符
                            if i == 0 or char_sequence[i - 1] not in target_chars:
                                score += 1
                            if i + len(target_chars) == len(char_sequence) or char_sequence[
                                i + len(target_chars)] not in target_chars:
                                score += 1
                            break

                if score > best_score:
                    best_score = score
                    best_match = sorted_chars[i:i + len(target_chars)] if score > 0 else None

        if best_match:
            # 计算整体中心坐标
            min_x = min(c['x'] for c in best_match)
            max_x = max(c['x'] + c['w'] for c in best_match)
            min_y = min(c['y'] for c in best_match)
            max_y = max(c['y'] + c['h'] for c in best_match)

            # 新增：检查周围区域是否有其他字符
            padding = 10  # 周围检查区域
            has_nearby_chars = False
            for char in found_chars:
                # 检查字符是否在目标区域附近但不在匹配组中
                if (char not in best_match and
                        (min_x - padding <= char['x'] <= max_x + padding) and
                        (min_y - padding <= char['y'] <= max_y + padding)):
                    has_nearby_chars = True
                    print("检查字符是否在目标区域附近但不在匹配组中")
                    break

            if not has_nearby_chars:
                center_x = (min_x + max_x) // 2
                center_y = (min_y + max_y) // 2
                print(f"找到'{button_name}'，中心坐标: ({center_x}, {center_y})")
                # 添加点击操作
                self.driver.tap([(center_x, center_y)], duration)
                print(f"✅ 已点击'{button_name}'按钮")
                return True
            else:
                print(f"⚠️ 找到'{button_name}'但周围有其他字符，跳过点击")
                return False
        else:
            print(f"未找到足够的目标字符来匹配'{button_name}'")
            return None

    def find_element(self, by=By.ID, value=None, timeout=15):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            print(f"⏱️ 超时未找到元素: {by}={value}")
            return None

    def click_element(self, by=By.ID, value=None):
        elem = self.find_element(by, value)
        if elem:
            elem.click()
            time.sleep(1.5)  # 延长点击后等待时间，让页面响应
            print(f"🖱️ 点击元素: {by}={value}")
            return True
        print(f"⚠️ 点击失败: 未找到元素 {by}={value}")
        return False

    def input_text(self, by=By.ID, value=None, text=""):
        elem = self.find_element(by, value)
        if elem:
            elem.clear()
            time.sleep(0.5)
            elem.send_keys(text)
            time.sleep(1.5)
            print(f"⌨️ 输入文本: '{text}' (元素: {by}={value})")
            return True
        print(f"⚠️ 输入失败: 未找到元素 {by}={value}")
        return False

    def click_text_on_screen(self, target_text, threshold=0.7, duration=300):
        """通过OCR识别屏幕上的文字并点击"""
        # 获取屏幕截图
        screenshot = self.driver.get_screenshot_as_png()
        screenshot_np = np.frombuffer(screenshot, np.uint8)
        screen = cv2.imdecode(screenshot_np, cv2.IMREAD_COLOR)

        # 转换为灰度图像
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        # 使用pytesseract进行OCR识别
        data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

        # 遍历识别结果
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            conf = int(data['conf'][i])

            # 如果识别到的文本匹配目标文本且置信度高于阈值
            if text and target_text.lower() in text.lower() and conf > threshold:
                # 获取文本位置
                x = data['left'][i]
                y = data['top'][i]
                w = data['width'][i]
                h = data['height'][i]

                # 计算中心点
                center_x = x + w // 2
                center_y = y + h // 2

                # 点击文字区域
                self.driver.tap([(center_x, center_y)], duration)
                print(f"✅ 通过OCR点击文字: '{text}' (置信度: {conf}) 位置: ({center_x}, {center_y})")
                return True

        print(f"❌ 未找到文字: '{target_text}'")
        return False

    # 返回点击主城
    def tap_by_percent(self, num=1, x_percent=0.07, y_percent=0.96, duration=300, desc="返回主城"):
        """按屏幕百分比点击"""
        window_size = self.driver.get_window_size()
        x = window_size['width'] * x_percent
        y = window_size['height'] * y_percent
        for i in range(num):
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) {desc}")
            sleep(0.5)
        return x, y

    # 领取vip经验
    def tap_by_vip(self, duration=300):
        """按屏幕百分比点击"""
        window_size = self.driver.get_window_size()
        # 点击主城
        self.tap_by_percent(5)
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:

            # 点击vip入口
            x = window_size['width'] * 0.07
            y = window_size['height'] * 0.1
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) vip入口")
            time.sleep(1)

            # 点击宝箱
            x = window_size['width'] * 0.94
            y = window_size['height'] * 0.24
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) 宝箱")
            time.sleep(1)

            # 点击领取
            x = window_size['width'] * 0.5
            y = window_size['height'] * 0.58
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) 点击领取按钮")
            time.sleep(1)

            print("vip经验已领取")
            return "已领取vip经验"
        else:
            print("流程异常跳过vip任务...")

    def tap_by_good_friend(self, duration=300, task_test="任务已完成"):
        """按屏幕百分比点击"""
        window_size = self.driver.get_window_size()
        # 点击主城
        self.tap_by_percent(5)
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            # 点击好友入口
            x = window_size['width'] * 0.07
            y = window_size['height'] * 0.78
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击好友入口")
            time.sleep(1)

            # 点击好友列表
            x = window_size['width'] * 0.89
            y = window_size['height'] * 0.95
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击好友列表")
            time.sleep(1)

            # 点击一键收送
            x = window_size['width'] * 0.83
            y = window_size['height'] * 0.85
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标({x:.0f}, {y:.0f}) 点击一键收送")
            time.sleep(1)

            return task_test
        else:
            print("好友流程异常跳过")

    # 聊天、军团
    def tap_by_chat(self, duration=300, task_test="任务已完成", text="t"):
        """按屏幕百分比点击"""
        window_size = self.driver.get_window_size()
        # 点击主城
        self.tap_by_percent(5)
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            # 点击聊天入口
            x = window_size['width'] * 0.07
            y = window_size['height'] * 0.82
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击聊天入口")
            time.sleep(1)

            # 点击世界
            x = window_size['width'] * 0.07
            y = window_size['height'] * 0.25
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击世界")
            time.sleep(1)

            # 聊天输入框
            x = window_size['width'] * 0.3
            y = window_size['height'] * 0.9
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标({x:.0f}, {y:.0f}) 点击发送消息")
            time.sleep(1)
            # 输入文本
            self.driver.execute_script('mobile: type', {'text': text})
            print(f"⌨️ 已输入文本: '{text}'")
            time.sleep(0.5)
            # 按下回车键
            self.driver.press_keycode(66)  # 66是回车键的keycode
            print("↵ 已按下回车键")
            time.sleep(0.5)

            # 点击发送消息
            x = window_size['width'] * 0.8
            y = window_size['height'] * 0.9
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标({x:.0f}, {y:.0f}) 点击发送消息")
            time.sleep(1)

            # 点击军团
            x = window_size['width'] * 0.07
            y = window_size['height'] * 0.3
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击军团")
            time.sleep(1)

            # 点击求助
            x = window_size['width'] * 0.68
            y = window_size['height'] * 0.83
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击求助")
            time.sleep(1)

            # 点击英雄碎片
            x = window_size['width'] * 0.23
            y = window_size['height'] * 0.36
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击英雄碎片")
            time.sleep(1)

            # 点击元宝
            x = window_size['width'] * 0.8
            y = window_size['height'] * 0.5
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击元宝")
            time.sleep(1)

            # 点击发布求助
            x = window_size['width'] * 0.5
            y = window_size['height'] * 0.7
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击发布求助")
            time.sleep(1)

            # 点击军团援助
            x = window_size['width'] * 0.83
            y = window_size['height'] * 0.83
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击求助")
            time.sleep(1)

            # 点击帮助
            for i in range(0, 5):
                x = window_size['width'] * 0.78
                y = window_size['height'] * 0.3
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击求助")
                time.sleep(1)

            return task_test

        else:
            print("军团援助异常pass")

    # 退出登录
    def outlogin(self, duration=1000):
        """按屏幕百分比点击"""

        window_size = self.driver.get_window_size()

        # 点击主城
        self.tap_by_percent(5)
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:

            # 点击头像
            x = window_size['width'] * 0.07
            y = window_size['height'] * 0.05
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) 点击头像")
            time.sleep(1)
            page_name = "./page_png/Settings.png"
            is_home = self.get_snapshot(file_path=page_name, compare=True)
            if is_home is True:
                # 点击设置
                x = window_size['width'] * 0.92
                y = window_size['height'] * 0.85
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) 设置")
                time.sleep(1)

                # 点击退出登录
                x = window_size['width'] * 0.5
                y = window_size['height'] * 0.63
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) 点击退出登录按钮")
                time.sleep(1)
            else:
                print("未找到设置按钮")
        else:
            print("退出登录流程异常")
            return False

    def gelogin(self, username, password, duration=300):
        page_name = "./page_png/login.png"
        is_login = self.get_snapshot(file_path=page_name, compare=True)
        if is_login is True:
            # 增加重试机制
            max_retries = 3
            retry_count = 0

            while retry_count < max_retries:
                try:
                    # 输入账号
                    account_field = self.find_element(
                        by=By.XPATH,
                        value="//android.widget.EditText[@hint='账号（6-36位数字或字母）']"
                    )
                    if account_field:
                        account_field.clear()
                        account_field.send_keys(username)

                    # 输入密码
                    password_field = self.find_element(
                        by=By.XPATH,
                        value="//android.widget.EditText[@hint='密码（6-18位数字或字母）']"
                    )
                    if password_field:
                        password_field.clear()
                        password_field.send_keys(password)

                    # 点击登录按钮
                    login_button = self.find_element(
                        by=By.XPATH,
                        value="//android.widget.Button[@text='登录']"
                    )
                    if login_button:
                        login_button.click()
                        break

                except Exception as e:
                    retry_count += 1
                    print(f"⚠️ 登录尝试 {retry_count}/{max_retries} 失败: {str(e)}")
                    time.sleep(1)
                    if retry_count == max_retries:
                        raise
            time.sleep(1)

            window_size = self.driver.get_window_size()

            # 点击同意服务条款
            print("\n🔄 点击同意服务条款...")
            x = window_size['width'] * 0.5  # 不是0.15就是0.16
            y = window_size['height'] * 0.7  # 不是0.24就是0.25
            self.driver.tap([(x, y)], 300)
            print(f"📍 已通过坐标 ({x}, {y})点击同意服务条款")
            self.tap_by_percent(2)
            time.sleep(1)

            # 点击跳过绑定手机号
            print("\n🔄 点击跳过绑定手机号...")
            x = window_size['width'] * 0.16  # 不是0.15就是0.16
            y = window_size['height'] * 0.24  # 不是0.24就是0.25
            self.driver.tap([(x, y)], 300)
            print(f"📍 已通过坐标 ({x}, {y})点击跳过绑定手机号")
            time.sleep(1)

            # 坐标点击进入游戏
            print("\n🔄 尝试通过坐标点击进入游戏按钮...")
            # 文字识别点击
            page_name = "./page_png/test.jpg"
            button_name = "进入游戏"
            self.find_game_entry(page_name, button_name)

            # 纯坐标点击（废弃）
            page_name = "./page_png/games_door.png"
            games_door = self.get_snapshot(file_path=page_name, compare=True)
            if games_door is True:
                x = window_size['width'] * 0.5
                y = window_size['height'] * 0.8
                self.driver.tap([(x, y)], 300)
                print(f"📍 已通过坐标点击 ({x}, {y})进入游戏")
                time.sleep(10)

            # 坐标点击关闭霸王弹窗1
            x = window_size['width'] * 0.85
            y = window_size['height'] * 0.28
            self.driver.tap([(x, y)], 300)
            print(f"📍 已通过坐标点击 ({x}, {y})关闭霸王弹窗1")
            time.sleep(1)

            # 坐标点击关闭霸王弹窗2
            x = window_size['width'] * 0.92
            y = window_size['height'] * 0.2
            self.driver.tap([(x, y)], 300)
            print(f"📍 已通过坐标点击 ({x}, {y})关闭霸王弹窗2")
            time.sleep(1)
            #
            self.tap_by_percent(3)
            time.sleep(1)
        else:
            print("登录流程异常")

    # 竞技场
    def page_leitai(self, duration=300):
        window_size = self.driver.get_window_size()
        # 点击主城
        self.tap_by_percent(5)
        # 判断是否在首页
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:

            # 初始化点击主城
            self.tap_by_percent(5)

            # 点击擂台入口
            print("\n🔄 点击同意服务条款...")
            x = window_size['width'] * 0.2
            y = window_size['height'] * 0.5
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击擂台入口")
            time.sleep(1)
            # 点击竞技场入口
            x = window_size['width'] * 0.2
            y = window_size['height'] * 0.2
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击竞技场入口")
            time.sleep(0.5)
            x = window_size['width'] * 0.5
            y = window_size['height'] * 0.86
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击挑战")

            x = window_size['width'] * 0.5
            y = window_size['height'] * 0.78
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击刷新对手")

            for i in range(5):
                time.sleep(1)
                x = window_size['width'] * 0.72
                y = window_size['height'] * 0.52
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x}, {y})点击挑战对手")
                time.sleep(1.5)
                x = window_size['width'] * 0.7
                y = window_size['height'] * 0.88
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x}, {y})点击返回玩法")

        else:
            print("竞技场流程异常")

    # 斗塔
    def page_douta(self, duration=300):
        window_size = self.driver.get_window_size()
        # 初始化点击主城
        self.tap_by_percent(5)
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            # 点击斗塔入口
            x = window_size['width'] * 0.4
            y = window_size['height'] * 0.5
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击斗塔入口")

            for i in range(3):
                # 点击挑战
                time.sleep(1)
                x = window_size['width'] * 0.5
                y = window_size['height'] * 0.85
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x}, {y})点击挑战")
                # 点击出战
                time.sleep(1)
                x = window_size['width'] * 0.66
                y = window_size['height'] * 0.85
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x}, {y})点击出战")
                time.sleep(1.3)
                x = window_size['width'] * 0.95
                y = window_size['height'] * 0.84
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x}, {y})点击跳过战斗")

                time.sleep(2)
                x = window_size['width'] * 0.25
                y = window_size['height'] * 0.87
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x}, {y})确定")

            # 点击每日奖励
            x = window_size['width'] * 0.95
            y = window_size['height'] * 0.3
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击每日奖励")
            time.sleep(0.5)
            # 点击领取
            x = window_size['width'] * 0.5
            y = window_size['height'] * 0.8
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击领取")

        else:
            print("斗塔流程异常")

    # 名将招募
    def page_zhaomu(self, duration=300):
        # 初始化点击主城
        self.tap_by_percent(5)
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            window_size = self.driver.get_window_size()
            # 点击招募入口
            x = window_size['width'] * 0.6
            y = window_size['height'] * 0.5
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击招募入口")

            # 获取招募页面截图

            # 点击招募
            time.sleep(0.5)
            x = window_size['width'] * 0.23
            y = window_size['height'] * 0.72
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击招募")

            time.sleep(20)
            self.tap_by_percent(5)
        else:
            print("名将招募异常")

    # 商店
    def page_store(self, duration=300):
        # 初始化点击主城
        self.tap_by_percent(5)
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            window_size = self.driver.get_window_size()
            # 点击商店入口
            time.sleep(0.5)
            x = window_size['width'] * 0.96
            y = window_size['height'] * 0.59
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击商店入口")
            time.sleep(0.5)
            x = window_size['width'] * 0.26
            y = window_size['height'] * 0.5
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击商店入口")

            time.sleep(0.5)
            x = window_size['width'] * 0.75
            y = window_size['height'] * 0.68
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击商店入口")

            time.sleep(0.5)
            x = window_size['width'] * 0.5
            y = window_size['height'] * 0.5
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击商店入口")

            time.sleep(0.5)
            x = window_size['width'] * 0.75
            y = window_size['height'] * 0.68
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击商店入口")
        else:
            print("商店流程异常")

    # 邮件
    def page_mail(self, duration=300):
        # 初始化点击主城
        self.tap_by_percent(5)
        window_size = self.driver.get_window_size()
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            pass

    # 军团
    def page_juntun(self, duration=300):
        # 初始化点击主城
        self.tap_by_percent(5)
        window_size = self.driver.get_window_size()
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            # 点击军团入口
            x = window_size['width'] * 0.07
            y = window_size['height'] * 0.3
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击军团入口")
            time.sleep(1)

            page_name = "./page_png/lianmeng.png"
            is_home = self.get_snapshot(file_path=page_name, compare=True)
            if is_home is True:
                # 点击军团、联盟入口
                x = window_size['width'] * 0.5
                y = window_size['height'] * 0.2
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击军团、联盟入口入口")
                time.sleep(1)

            x = window_size['width'] * 0.36
            y = window_size['height'] * 0.72
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击祭祀入口")
            time.sleep(1)

            x = window_size['width'] * 0.5
            y = window_size['height'] * 0.78
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击祭祀")
            time.sleep(1)

            x = window_size['width'] * 0.7
            y = window_size['height'] * 0.6
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击祭祀确定")
            time.sleep(1)

            for i in range(2):
                x = window_size['width'] * 0.91
                y = window_size['height'] * 0.19
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击关闭祭祀页面")

            x = window_size['width'] * 0.52
            y = window_size['height'] * 0.55
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击军团副本入口")

            for i in range(2):
                x = window_size['width'] * 0.5
                y = window_size['height'] * 0.88
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击挑战")

                x = window_size['width'] * 0.7
                y = window_size['height'] * 0.85
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击出战")

                time.sleep(1.3)
                x = window_size['width'] * 0.95
                y = window_size['height'] * 0.84
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x}, {y})点击跳过战斗")

                time.sleep(1.5)
                x = window_size['width'] * 0.7
                y = window_size['height'] * 0.88
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x}, {y})点击返回玩法")

            self.tap_by_percent(1)

            # 点击盟主挑战切磋
            time.sleep(1)
            x = window_size['width'] * 0.15
            y = window_size['height'] * 0.7
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击盟主雕像")

            x = window_size['width'] * 0.60
            y = window_size['height'] * 0.86
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击切磋")

            time.sleep(1)
            x = window_size['width'] * 0.7
            y = window_size['height'] * 0.85
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击出战")

            time.sleep(1.3)
            x = window_size['width'] * 0.95
            y = window_size['height'] * 0.84
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击跳过战斗")
            time.sleep(1.5)
            x = window_size['width'] * 0.25
            y = window_size['height'] * 0.88
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击确定战斗结果")

    # 野外
    def page_yewai(self, duration=300):
        window_size = self.driver.get_window_size()
        # 初始化点击主城
        self.tap_by_percent(3)
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            time.sleep(0.5)
            x = window_size['width'] * 0.76
            y = window_size['height'] * 0.94
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击野外入口")

            time.sleep(0.5)
            x = window_size['width'] * 0.3
            y = window_size['height'] * 0.5
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击火烧赤壁入口")

            time.sleep(0.5)
            x = window_size['width'] * 0.9
            y = window_size['height'] * 0.7
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击一键扫荡入口")

            time.sleep(0.5)
            x = window_size['width'] * 0.5
            y = window_size['height'] * 0.65
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击扫荡")

            # 点击返回按钮
            self.tap_by_percent()

            page_name = "./page_png/outdoors1.png"
            outdoors = self.get_snapshot(file_path=page_name, compare=True)
            if outdoors is True:
                time.sleep(0.5)
                x = window_size['width'] * 0.3
                y = window_size['height'] * 0.2
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x}, {y})点击副本入口")

                # button_name = "扫荡"
                # self.find_game_entry(button_name)

                time.sleep(0.5)
                x = window_size['width'] * 0.55
                y = window_size['height'] * 0.93
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x}, {y})点击装备副本入口")
                time.sleep(0.5)

                for i in range(3):
                    time.sleep(0.5)
                    x = window_size['width'] * 0.85
                    y = window_size['height'] * 0.45
                    self.driver.tap([(x, y)], 0)
                    print(f"📍 已通过坐标 ({x}, {y})点击扫荡")

                    page_name = "./page_png/fuben_saodang_tishi.png"
                    outdoors = self.get_snapshot(file_path=page_name, compare=True, threshold=0.5)
                    if outdoors is True:
                        time.sleep(0.5)
                        x = window_size['width'] * 0.7
                        y = window_size['height'] * 0.60
                        self.driver.tap([(x, y)], 10)
                        print(f"📍 已通过坐标 ({x}, {y})点击扫荡")

                    time.sleep(0.5)
                    self.tap_by_percent()

        elif is_home is False:
            print("副本页面不匹配")
        else:
            print("未知错误")

    # 征战
    def page_zhengzhan(self, duration=300):
        window_size = self.driver.get_window_size()
        # 初始化点击主城
        self.tap_by_percent(5)

        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True, threshold=0.5)
        if is_home is True:
            # 文字识别点击征战
            page_name = "./page_png/home.png"
            button_name = "征战"
            self.find_game_entry(page_name, button_name)

            # 点击征战收益
            time.sleep(0.5)
            x = window_size['width'] * 0.2
            y = window_size['height'] * 0.7
            self.driver.tap([(x, y)], 10)
            print(f"📍 已通过坐标 ({x}, {y})点击征战收益")

            time.sleep(1)
            page_name = "./page_png/zhengzhan_shouyi.png"
            zhengzhan_shouyi = self.get_snapshot(file_path=page_name, compare=True)
            if zhengzhan_shouyi is True:
                time.sleep(0.5)
                x = window_size['width'] * 0.7
                y = window_size['height'] * 0.83
                self.driver.tap([(x, y)], 10)
                print(f"📍 已通过坐标 ({x}, {y})点击领取收益")
                time.sleep(2)
                # 判断领取收益页面
                page_name = "./page_png/guaji_jiangli.png"
                guaji_jiangli = self.get_snapshot(file_path=page_name, compare=True, page_name="领取收益")
                if guaji_jiangli is True:
                    self.tap_by_percent(1)

                    time.sleep(5)
                    # 判断升级页面
                    page_name = "./page_png/shengji.png"
                    shengji = self.get_snapshot(file_path=page_name, compare=True, page_name="升级")
                    if shengji is True:
                        self.tap_by_percent(1)

                time.sleep(1)
                for i in range(5):
                    if i == 2:
                        time.sleep(5)
                    x = window_size['width'] * 0.3
                    y = window_size['height'] * 0.83
                    self.driver.tap([(x, y)], 10)
                    print(f"📍 已通过坐标 ({x}, {y})点击快速探采")
                    time.sleep(1)

                    page_name = "./page_png/shouyi_tancai.png"
                    shouyi_tancai = self.get_snapshot(file_path=page_name, compare=True, threshold=0.7,
                                                      page_name="快速探采")
                    if shouyi_tancai is True:
                        time.sleep(1)
                        x = window_size['width'] * 0.5
                        y = window_size['height'] * 0.73
                        self.driver.tap([(x, y)], 10)
                        print(f"📍 已通过坐标 ({x}, {y})点击快速收益")



            else:
                print("未找到领取收益/快速探采")



        elif is_home is False:
            print("副本页面不匹配")
        else:
            print("未知错误")

    # 完成任务
    def page_task(self, duration=300):
        # 初始化点击主城
        self.tap_by_percent(5)
        window_size = self.driver.get_window_size()
        # 点击任务入口
        time.sleep(0.5)
        x = window_size['width'] * 0.95
        y = window_size['height'] * 0.72
        self.driver.tap([(x, y)], duration)
        print(f"📍 已通过坐标 ({x}, {y})点击任务入口")
        time.sleep(1)
        page_name = "./page_png/daily_tasks.png"
        daily_tasks = self.get_snapshot(file_path=page_name, compare=True, threshold=0.7, page_name="日常任务页面")
        if daily_tasks is True:
            x = window_size['width'] * 0.5
            y = window_size['height'] * 0.88
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击一键领取任务奖励")

    # 活动
    def activity(self):
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            # 文字识别点击

            button_name = "野外"
            self.find_game_entry(button_name=button_name)

    def get_run(self, username):
        print("\n🔐 开始登录流程...")
        try:
            # 调取登录方法输入账号密码登录
            self.gelogin(username=username, password="python")

            # 领取vip奖励
            self.tap_by_vip()
            time.sleep(1)

            # 点击主城
            self.tap_by_percent(1)
            time.sleep(1)

            # 点击好友收送
            self.tap_by_good_friend()
            # 聊天、军团派遣
            self.tap_by_chat()
            self.page_leitai()
            self.page_douta()

            self.page_zhaomu()
            self.page_store()
            # self.page_mail()
            self.page_juntun()

            self.page_yewai()
            self.page_zhengzhan()
            self.page_task()

            # 退出登录
            self.outlogin()
            print("脚本结束")

        except Exception as e:
            print(f"\n❌ 登录流程异常: {str(e)}")

    def quit(self):
        if self.driver:
            try:
                self.driver.quit()
                print("\n🛑 驱动已关闭")
            except Exception as e:
                print(f"\n⚠️ 关闭驱动时出错: {str(e)}")

    def get_snapshot(self, file_path=None, compare=None, threshold=0.7, page_name="test"):
        # 保存截图传file_path, 两图比较传file_path 和 compare
        # 获取当前屏幕截图
        screenshot = self.driver.get_screenshot_as_png()
        screenshot_np = np.frombuffer(screenshot, np.uint8)
        screen = cv2.imdecode(screenshot_np, cv2.IMREAD_COLOR)
        if file_path and compare is None:
            if not os.path.exists(file_path):  # 检查文件是否已存在
                with open(file_path, 'wb') as file:
                    file.write(screenshot)
                    print("✅ 截图已保存")
            else:
                print("⚠️ 截图文件已存在，跳过保存")
        else:
            print('file_path is None')

        if compare and file_path is not None:
            template = cv2.imread(file_path, cv2.IMREAD_COLOR)  # 改为军团相关模板
            if template is None:
                print(f"❌ 无法加载{page_name}模板图像")

            # 进行模板匹配
            result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # 设置匹配阈值 # 提高阈值减少误匹配
            if max_val >= threshold:
                # 匹配值
                print(f"✅ 通过图像匹配点击{page_name}按钮 (置信度: {max_val:.2f})")
                time.sleep(1)
                return True
            else:
                print(f"❌ 未找到匹配的{page_name}按钮 (最高置信度: {max_val:.2f})")
        else:
            print('compare is None')
            return 'compare is None'

        return screen

