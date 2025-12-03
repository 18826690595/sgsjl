import time
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


class Utils():

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
    
    # 在appium_init方法中增加连接检查
    def appium_init(self, max_retries=3):
        print("⚙️ 正在初始化Appium驱动...")
        caps = UiAutomator2Options()
        caps.set_capability("appium:deviceName", self.device_id)
        caps.set_capability("appium:appPackage", self.package_name)
        caps.set_capability("appium:appActivity", ".MainActivity")
        caps.set_capability("appium:automationName", "UiAutomator2")
        caps.set_capability("appium:noReset", True)
        caps.set_capability("appium:newCommandTimeout", 300)  # 增加命令超时时间
        
        appium_server_url = "http://127.0.0.1:4723"
        
        for attempt in range(max_retries):
            try:
                self.driver = webdriver.Remote(appium_server_url, options=caps)
                # 增加连接检查
                try:
                    self.driver.get_window_size()  # 测试连接是否正常
                except:
                    raise Exception("Appium连接不稳定")
                    
                self.driver.implicitly_wait(15)
                print(f"✅ Appium驱动初始化成功 - 服务器: {appium_server_url}")
                return True
            except Exception as e:
                print(f"❌ Appium连接失败(尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # 等待2秒后重试
                    continue
                raise  # 最后一次尝试失败后抛出异常


    # 图片识别处理提取文本
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




    # 在get_snapshot方法中修改重试逻辑
    def get_snapshot(self, file_path=None, compare=None, threshold=0.7, page_name="test"):
        # 保存截图传file_path, 两图比较传file_path 和 compare
        if not self.driver:
            print("⚠️ 错误: driver未初始化")
            return False

        max_retries = 3
        screenshot = None
        for attempt in range(max_retries):
            try:
                screenshot = self.driver.get_screenshot_as_png()
                break  # 如果成功则跳出循环
            except Exception as e:
                print(f"⚠️ 获取截图失败(尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    print("🔄 尝试重新初始化Appium驱动...")
                    self.appium_init()
                    time.sleep(2)  # 等待2秒后重试
                    continue
                print("❌ 重试次数用尽，无法获取截图")
                return False

        if screenshot is None:
            return False

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

            try:
                window_size = self.driver.get_window_size()
            except Exception as e:
                print(f"⚠️ 获取窗口尺寸失败: {str(e)}")
                print("🔄 尝试重新初始化Appium驱动...")
                self.appium_init()
                try:
                    window_size = self.driver.get_window_size()
                except Exception as e:
                    print(f"❌ 重连失败: {str(e)}")
                    return False

            x = window_size['width'] * width
            y = window_size['height'] * height
            
            # # 修改点击方式为TouchAction
            # from appium.webdriver.common.touch_action import TouchAction
            # action = TouchAction(self.driver)
            # action.tap(x=x, y=y).perform()
            self.driver.tap([(x, y)], 1)
            print(f"📍 已通过坐标 ({x}, {y})点击")
            time.sleep(0.5)  # 添加短暂延迟确保操作完成
            
            if input_text is not None and press_keycode is not None:
                # 输入文本
                self.driver.execute_script('mobile: type', {'text': input_text})
                self.driver.press_keycode(press_keycode)
                print(f"📍 已通过坐标 ({x}, {y})输入{input_text}内容")
                
            return True
        except Exception as e:
            print(f"❌ 坐标点击失败: {str(e)}")
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
                is_home = self.get_snapshot(file_path="./page_png/home.png", compare=True, page_name="主城")
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


    def Page_Login(self, username, password="python"):
        try:
            is_login = self.get_snapshot(file_path="./page_png/login.png", compare=True)
            if is_login is True:
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
                # # 输入账号
                # self.coordinates(width=0.5, height=0.4, input_text=username)
                #
                # # 输入密码
                # self.coordinates(width=0.5, height=0.5, input_text=password)
                # # 点击登录
                # self.coordinates(width=0.5, height=0.6)
                time.sleep(0.5)
                # 同意服务条款
                self.coordinates(width=0.5, height=0.7)
                time.sleep(0.5)
                # 跳过手机号绑定
                self.coordinates(width=0.16, height=0.24)

                # 确认进入游戏页面
                for i in range(10):
                    time.sleep(0.5)
                    games_door = self.get_snapshot(file_path="./page_png/games_door.png", compare=True)
                    if games_door is False:
                        self.coordinates(width=0.07, height=0.96)
                time.sleep(0.5)
                # 点击进入游戏
                self.coordinates(width=0.5, height=0.8)
                time.sleep(3)

                # 关闭弹窗(需要增加判断是否出现弹窗)
                for i in range(15):
                    tanchuang2 = self.get_snapshot(file_path="./page_png/tanchuang2.png", compare=True)
                    if tanchuang2 is True:
                        self.coordinates(width=0.85, height=0.28)
                        self.coordinates(width=0.92, height=0.2)
                    else:
                        time.sleep(1)
            else:
                print("❌ 无法确认登录页面状态")
                return False

        except Exception as e:
            print(f"❌ 登录流程出错: {str(e)}")
            raise
        
    # 领取vip经验
    def Page_Vip(self):
        """按屏幕百分比点击"""
        # 点击主城
        is_home = self.Page_Percent(5)
        try:
            if is_home:  # 修复条件判断
                try:
                    # 点击vip入口
                    self.coordinates(width=0.07, height=0.1)
                    # 点击宝箱
                    self.coordinates(width=0.94, height=0.24)
                    # 点击领取
                    self.coordinates(width=0.5, height=0.58)

                    print("vip经验已领取")
                    return True
                except Exception as e:
                    print(f"执行vip任务时出错: {str(e)}")
                    # 可以添加driver重启逻辑
                    return False
        except Exception as e:
            print(f"执行流程时出错: {str(e)}")
            return False


    # 聊天、军团
    def Page_Chat(self, text="1"):
        """按屏幕百分比点击"""
        # 点击主城
        self.Page_Percent(5)
        is_home = self.get_snapshot(file_path="./page_png/home.png", compare=True)
        if is_home is True:
            # 点击聊天入口
            self.coordinates(width=0.07, height=0.82)
            time.sleep(1)

            # 点击世界
            self.coordinates(width=0.07, height=0.25)
            time.sleep(1)

            # 聊天输入框
            self.coordinates(width=0.3, height=0.9)
            time.sleep(1)
            # 输入文本
            self.coordinates(width=0.3, height=0.9, input_text=text, press_keycode=66)
            # self.driver.press_keycode(66)  # 66是回车键的keycode
            time.sleep(0.5)

            # 点击发送消息
            self.coordinates(width=0.8, height=0.9)
            time.sleep(1)

            # 点击军团
            self.coordinates(width=0.07, height=0.3)
            time.sleep(1)

            # 点击求助
            self.coordinates(width=0.68, height=0.83)
            time.sleep(1)

            # 点击英雄碎片
            self.coordinates(width=0.23, height=0.36)
            time.sleep(1)

            # 点击元宝
            self.coordinates(width=0.8, height=0.5)
            time.sleep(1)

            # 点击发布求助
            self.coordinates(width=0.5, height=0.7)
            time.sleep(1)

            # 点击军团援助
            self.coordinates(width=0.83, height=0.83)
            time.sleep(1)

            # 点击帮助
            for i in range(5):
                self.coordinates(width=0.78, height=0.3)

            return True

        else:
            print("军团援助异常pass")
            return False

     # 好友日常任务
    def Page_good_friend(self):
        """按屏幕百分比点击"""
        # 点击主城
        self.Page_Percent(5)
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            # 点击好友入口
            self.coordinates(width=0.07, height=0.78)
            time.sleep(1)

            # 点击好友列表
            self.coordinates(width=0.89, height=0.95)
            time.sleep(1)

            # 点击一键收送
            self.coordinates(width=0.83, height=0.85)
            time.sleep(1)

            return True
        else:
            print("好友流程异常跳过")


     # 竞技场
    def Page_Arena(self, duration=300):
        # 点击主城
        self.Page_Percent(5)
        # 判断是否在首页
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            # 点击擂台入口
            # print("\n🔄 点击同意服务条款...")
            # x = window_size['width'] * 0.2
            # y = window_size['height'] * 0.5
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x}, {y})点击擂台入口")
            self.coordinates(width=0.2, height=0.5)
            time.sleep(1)
            # 点击竞技场入口
            # x = window_size['width'] * 0.2
            # y = window_size['height'] * 0.2
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x}, {y})点击竞技场入口")
            self.coordinates(width=0.2, height=0.2)
            time.sleep(0.5)
            # x = window_size['width'] * 0.5
            # y = window_size['height'] * 0.86
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x}, {y})点击挑战")
            self.coordinates(width=0.5, height=0.86)

            # x = window_size['width'] * 0.5
            # y = window_size['height'] * 0.78
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x}, {y})点击刷新对手")
            self.coordinates(width=0.5, height=78)

            for i in range(5):
                time.sleep(1)
                # x = window_size['width'] * 0.72
                # y = window_size['height'] * 0.52
                # self.driver.tap([(x, y)], duration)
                # print(f"📍 已通过坐标 ({x}, {y})点击挑战对手")
                self.coordinates(width=0.72, height=0.52)
                time.sleep(1.5)
                # x = window_size['width'] * 0.7
                # y = window_size['height'] * 0.88
                # self.driver.tap([(x, y)], duration)
                # print(f"📍 已通过坐标 ({x}, {y})点击返回玩法")
                self.coordinates(width=0.7, height=0.88)

        else:
            print("竞技场流程异常")


    # 斗塔
    def Page_Trials_Tower(self, duration=300):
        # window_size = self.driver.get_window_size()
        # 初始化点击主城
        self.Page_Percent(5)
        is_home = self.get_snapshot(file_path="./page_png/home.png", compare=True)
        if is_home is True:
            # 点击斗塔入口
            self.coordinates(width=0.4, height=0.5)
            for i in range(3):
                # 点击挑战
                time.sleep(1)
                self.coordinates(width=0.5, height=0.85)

                # 点击出战
                time.sleep(1)
                self.coordinates(width=0.66, height=0.85)

                time.sleep(1.3)
                self.coordinates(width=0.95, height=0.84)

                time.sleep(2)
                self.coordinates(width=0.25, height=0.87)
            # 点击每日奖励
            self.coordinates(width=0.95, height=0.3)
            time.sleep(0.5)
            # 点击领取
            self.coordinates(width=0.5, height=0.8)

        else:
            print("斗塔流程异常")


     # 名将招募
    def Page_Recruit(self, duration=300):
        # 初始化点击主城
        self.Page_Percent(5)
        is_home = self.get_snapshot(file_path="./page_png/home.png", compare=True)
        if is_home is True:
            # 点击招募入口
            self.coordinates(width=0.6, height = 0.5)

            # 获取招募页面截图

            # 点击招募
            time.sleep(0.5)
            self.coordinates(width=0.23, height = 0.72)
            zhaomu_chenggong = self.get_snapshot(file_path="./page_png/zhaomu_chenggong.png", compare=True, page_name="招募成功")
            if zhaomu_chenggong is True:
                self.coordinates(width=0.1, height = 0.87)
            # 返回首页
            self.Page_Percent(20)
        else:
            print("名将招募异常")

    # 商店
    def Page_Store(self, duration=300):
        # 初始化点击主城
        self.Page_Percent(5)
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            # 点击商店入口
            time.sleep(0.5)
            self.coordinates(width=0.96, height=0.59)
            time.sleep(0.5)
            self.coordinates(width=0.26, height = 0.5)

            time.sleep(0.5)
            self.coordinates(width=0.75, height = 0.68)

            time.sleep(0.5)
            self.coordinates(width=0.5, height = 0.5)

            time.sleep(0.5)
            self.coordinates(width=0.75, height = 0.68)
        else:
            print("商店流程异常")


    # 军团
    def Page_Legion(self, duration=300):
        # 初始化点击主城
        self.Page_Percent(5)
        is_home = self.get_snapshot(file_path="./page_png/home.png", compare=True)
        if is_home is True:
            # 点击军团入口
            self.coordinates(width=0.58, height=0.96)
            # x = window_size['width'] * 0.5
            # y = window_size['height'] * 0.2
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击军团入口")
            time.sleep(1)

            is_home = self.get_snapshot(file_path="./page_png/lianmeng.png", compare=True)
            if is_home is True:
                # 点击军团、联盟入口
                self.coordinates(width=0.5, height=0.2)
                # x = window_size['width'] * 0.5
                # y = window_size['height'] * 0.2
                # self.driver.tap([(x, y)], duration)
                # print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击军团、联盟入口入口")
                time.sleep(1)


            self.coordinates(width=0.36, height=0.72)
            # x = window_size['width'] * 0.36
            # y = window_size['height'] * 0.72
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击祭祀入口")
            time.sleep(1)

            self.coordinates(width=0.5, height=0.78)
            # x = window_size['width'] * 0.5
            # y = window_size['height'] * 0.78
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击祭祀")
            time.sleep(1)

            self.coordinates(width=0.7, height=0.6)
            # x = window_size['width'] * 0.7
            # y = window_size['height'] * 0.6
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击祭祀确定")
            time.sleep(1)

            for i in range(2):
                self.coordinates(width=0.91, height=0.19)

                # x = window_size['width'] * 0.91
                # y = window_size['height'] * 0.19
                # self.driver.tap([(x, y)], duration)
                # print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击关闭祭祀页面")

            self.coordinates(width=0.52, height=0.55)

            # x = window_size['width'] * 0.52
            # y = window_size['height'] * 0.55
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击军团副本入口")

            for i in range(2):
                self.coordinates(width=0.5, height=0.88)

                # x = window_size['width'] * 0.5
                # y = window_size['height'] * 0.88
                # self.driver.tap([(x, y)], duration)
                # print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击挑战")

                self.coordinates(width=0.7, height=0.85)

                time.sleep(1.3)
                self.coordinates(width=0.95, height=0.84)
                time.sleep(1.5)
                self.coordinates(width=0.7, height=0.88)

            # 点击返回
            self.coordinates(width=0.07, height=0.96)

            # 点击盟主挑战切磋
            time.sleep(1)
            self.coordinates(width=0.15, height=0.7)

            self.coordinates(width=0.60, height=0.86)

            time.sleep(1)
            self.coordinates(width=0.7, height=0.85)

            time.sleep(1.3)
            self.coordinates(width=0.95, height=0.84)

            time.sleep(1.5)
            self.coordinates(width=0.25, height=0.88)


    # 野外
    def Page_OutDoors(self, duration=300):
        # 初始化点击主城
        self.Page_Percent(10)
        is_home = self.get_snapshot(file_path="./page_png/home.png", compare=True)
        if is_home is True:
            time.sleep(0.5)
            self.coordinates(width=0.76, height = 0.94)

            time.sleep(0.5)
            self.coordinates(width=0.3, height = 0.5)

            time.sleep(0.5)
            self.coordinates(width=0.9, height = 0.7)

            time.sleep(0.5)
            self.coordinates(width=0.5, height = 0.65)

            # 点击返回按钮
            # self.tap_by_percent()
            for i in range(2):
                self.coordinates(width=0.07, height = 0.96)
                time.sleep(0.5)

                outdoors = self.get_snapshot(file_path="./page_png/outdoors1.png", compare=True)
                if outdoors is True:
                    time.sleep(0.5)
                    self.coordinates(width=0.3, height=0.2)

                    time.sleep(0.5)
                    self.coordinates(width=0.55, height=0.93)
                    time.sleep(0.5)

                    # 循环扫荡3次
                    for i in range(6):
                        time.sleep(0.5)
                        self.coordinates(width=0.85, height=0.45)

                        outdoors = self.get_snapshot(file_path="./page_png/fuben_saodang_tishi.png", compare=True, threshold=0.5)
                        if outdoors is True:
                            time.sleep(0.5)
                            self.coordinates(width=0.7, height=0.60)
                        time.sleep(0.5)
                        # self.tap_by_percent()
                        self.coordinates(width=0.07, height=0.96)

        elif is_home is False:
            print("副本页面不匹配")
        else:
            print("未知错误")


    # 征战
    def Page_Campaign(self):
        # 初始化点击主城
        self.Page_Percent(5)

        is_home = self.get_snapshot(file_path="./page_png/home.png", compare=True, threshold=0.5)
        if is_home is True:
            # 文字识别点击征战
            page_name = "./page_png/home.png"
            button_name = "征战"
            self.find_game_entry(page_name, button_name)

            # 点击征战收益
            time.sleep(0.5)
            self.coordinates(width=0.2, height=0.7)
            time.sleep(1)

            # 判断当前是否在征战收益页面
            zhengzhan_shouyi = self.get_snapshot(file_path="./page_png/zhengzhan_shouyi.png", compare=True)
            if zhengzhan_shouyi is True:
                self.coordinates(width=0.7, height=0.83)
                time.sleep(1)
                # 判断游历值溢出页面
                youli_yichu = self.get_snapshot(file_path="./page_png/youli_yichu.png", compare=True, threshold=0.7, page_name="收益溢出")
                if youli_yichu is True:
                    self.coordinates(width=0.7, height=0.63)
                # 判断领取收益页面
                guaji_jiangli = self.get_snapshot(file_path="./page_png/guaji_jiangli.png", compare=True, page_name="领取收益")
                if guaji_jiangli is True:
                    self.coordinates(width=0.07, height=0.96)

                    time.sleep(5)
                    # 判断升级页面
                    shengji = self.get_snapshot(file_path="./page_png/shengji.png", compare=True, page_name="升级")
                    if shengji is True:
                        self.coordinates(width=0.07, height=0.96)

                time.sleep(1)

                # 循环快速采摘
                for i in range(5):
                    # 第一次点击
                    if i == 2:
                        time.sleep(5)
                    self.coordinates(width=0.3, height=0.83)
                    time.sleep(1)

                    shouyi_tancai = self.get_snapshot(file_path="./page_png/shouyi_tancai.png", compare=True, threshold=0.7, page_name="快速探采")
                    if shouyi_tancai is True:
                        self.coordinates(width=0.5, height=0.73)
                        time.sleep(0.5)

                        # 判断游历值溢出页面
                        youli_yichu = self.get_snapshot(file_path="./page_png/youli_yichu.png", compare=True, threshold=0.7, page_name="收益溢出")
                        if youli_yichu is True:
                            self.coordinates(width=0.7, height=0.63)



            else:
                print("未找到领取收益/快速探采")



        elif is_home is False:
            print("副本页面不匹配")
        else:
            print("未知错误")

    # 完成任务
    def Page_Task(self, duration=300):
        # 初始化点击主城
        self.Page_Percent(5)
        # 点击任务入口
        time.sleep(0.5)
        self.coordinates(width=0.95, height=0.72)
        time.sleep(1)
        page_name = "./page_png/daily_tasks.png"
        daily_tasks = self.get_snapshot(file_path=page_name, compare=True, threshold=0.7, page_name="日常任务页面")
        if daily_tasks is True:
            self.coordinates(width=0.5, height=0.88)
            print(f"📍 已通过坐标点击一键领取任务奖励")
    

    # 退出登录
    def Page_Out_Login(self, duration=1000):
        """按屏幕百分比点击"""

        # 点击主城
        self.Page_Percent(5)
        is_home = self.get_snapshot(file_path="./page_png/home.png", compare=True)
        if is_home is True:
            # 点击头像
            self.coordinates(width=0.07, height = 0.05)
            time.sleep(1)
            is_home = self.get_snapshot(file_path="./page_png/Settings.png", compare=True)
            if is_home is True:
                # 点击设置
                self.coordinates(width=0.92, height=0.85)
                time.sleep(1)

                # 点击退出登录
                self.coordinates(width=0.5, height=0.63)
                time.sleep(1)
            else:
                print("未找到设置按钮")
        else:
            print("退出登录流程异常")
            return False


    def get_run(self):
        """主运行方法"""
        for i in range(202508001, 202508029):
            print("===============")
            self.Page_Login(username=i, password="python")
            self.Page_Vip()
            self.Page_good_friend()
            self.Page_Chat()
            self.Page_Arena()
            self.Page_Trials_Tower()
            self.Page_Recruit()
            self.Page_Store()
            self.Page_Legion()
            self.Page_OutDoors()
            self.Page_Campaign()
            self.Page_Task()


            self.Page_Out_Login()

            break
            # 点击主城
            # self.tap_by_percent.Page_Percent()

    


if __name__ == "__main__":
# try:
    # 删除这行，不需要单独创建 Locators 实例
    # app_manager = Locators()
    run = Utils()
    run.get_run()
# except Exception as e:
#     print(e)
# finally:
    # 修改为使用 run 实例中的驱动
    if 'run' in locals():
        run.quit()  # 确保 Locators 类中有 quit() 方法