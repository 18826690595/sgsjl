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


class Utils:
    _instance = None  # 添加类变量用于单例模式
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Utils, cls).__new__(cls)
        return cls._instance

    def __init__(self, device_id="127.0.0.1:7555", package_name="com.wxbz_sgshjz.ks10"):
        if hasattr(self, 'driver') and self.driver:  # 如果已经初始化则跳过
            return
            
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

        return False

    def coordinates(self, width, height, input_text=None, press_keycode=None):
        try:
            if not self.driver:
                print("⚠️ 错误: driver未初始化")
                return False
            window_size = self.driver.get_window_size()
            if input_text is None:
                # 输入信息
                x = window_size['width'] * width
                y = window_size['height'] * height
                self.driver.tap([(x, y)], 10)
                print(f"📍 已通过坐标 ({x}, {y})点击")
                return True
            if input_text is not None and press_keycode is not None:
                # 输入信息
                print("\n🔄 正在点击...")
                x = window_size['width'] * width
                y = window_size['height'] * height
                self.driver.tap([(x, y)], 10)
                time.sleep(0.5)

                # Ctrl+A
                # self.driver.press_keycode(29, 28672)
                # self.driver.execute_script('mobile: type', {'text': ""})
                time.sleep(0.5)
                self.driver.execute_script('mobile: type', {'text': input_text})
                self.driver.press_keycode(press_keycode)
                print(f"📍 已通过坐标 ({x}, {y})输入{input_text}内容")
                return True
        except Exception as e:
            print(e)
            return False




    def quit(self):
        """退出方法"""
        self.driver.quit()



    def lgs(self):
        print("test")

    # 返回点击主城
    def Page_Percent(self, num=5, x_percent=0.07, y_percent=0.96):
        """按屏幕百分比点击"""
        try:
            for i in range(num):
                is_home = self.get_snapshot(file_path="../page_png/home.png", compare=True, page_name="主城")
                if is_home is True:
                    # 如果在首页则返回True
                    return True
                elif is_home is False:
                    self.coordinates(width=x_percent, height=y_percent)
                    time.sleep(0.5)
                else:
                    print("未知错误")
            return False
        except Exception as e:
            print(e)
            return False








# 修改测试部分
if __name__ == "__main__":
    test = Utils()
    # test.get_snapshot(file_path="../page_png/home.png", compare=True)
    # time.sleep(0.5)
    # test.coordinates(width=0.92, height=0.2)
    file_path = '../page_png/zhaomu_chenggong.png'
    # app_manager.get_snapshot(file_path,1)
    test.get_snapshot(file_path)