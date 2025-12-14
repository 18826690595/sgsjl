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


class Utils():

    def __init__(self, driver):
        self.driver = driver
        # 初始化时获取一次窗口尺寸
        try:
            self.window_size = self.driver.get_window_size()
            print(f"✅ 已获取窗口尺寸: {self.window_size}")
        except Exception as e:
            print(f"❌ 获取窗口尺寸失败: {str(e)}")
            self.window_size = {'width': 1920, 'height': 1080}  # 默认值


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




    def click_icon(self, icon_path, threshold=0.5, duration=0):
        """
        识别并点击屏幕上的图标
        :param icon_path: 图标模板图片路径
        :param threshold: 匹配阈值 (0-1)
        :param duration: 点击持续时间(毫秒)
        :return: 是否找到并点击了图标
        """
        try:
            # 获取屏幕截图
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_np = np.frombuffer(screenshot, np.uint8)
            screen = cv2.imdecode(screenshot_np, cv2.IMREAD_COLOR)
            
            # 读取图标模板
            template = cv2.imread(icon_path, cv2.IMREAD_COLOR)
            if template is None:
                print(f"❌ 无法加载图标模板: {icon_path}")
                return False
                
            # 图像预处理 - 增强对比度
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            
            # 直方图均衡化
            screen_gray = cv2.equalizeHist(screen_gray)
            template_gray = cv2.equalizeHist(template_gray)
            
            # 多尺度模板匹配
            found = None
            for scale in np.linspace(0.8, 1.2, 5):  # 在80%-120%范围内缩放
                resized = cv2.resize(template_gray, 
                                    (int(template.shape[1] * scale), 
                                     int(template.shape[0] * scale)))
                
                # 确保模板不大于屏幕图像
                if resized.shape[0] > screen_gray.shape[0] or resized.shape[1] > screen_gray.shape[1]:
                    continue
                    
                # 模板匹配
                result = cv2.matchTemplate(screen_gray, resized, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                # 更新最佳匹配
                if found is None or max_val > found[0]:
                    found = (max_val, max_loc, scale)
            
            if found is None or found[0] < threshold:
                # 修复格式说明符错误
                print(f"❌ 未找到匹配的图标 (最高置信度: {found[0] if found else 0:.2f})")
                return False
                
            max_val, max_loc, scale = found
            
            # 计算图标中心位置 (考虑缩放因子)
            h, w = template.shape[:2]
            scaled_w = int(w * scale)
            scaled_h = int(h * scale)
            center_x = max_loc[0] + scaled_w // 2
            center_y = max_loc[1] + scaled_h // 2
            
            # 二次验证 - 检查匹配区域周围
            roi = screen_gray[max_loc[1]:max_loc[1]+scaled_h, max_loc[0]:max_loc[0]+scaled_w]
            _, binary = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            white_pixels = np.sum(binary == 255)
            black_pixels = np.sum(binary == 0)
            
            # 如果匹配区域大部分是空白或全黑，可能是误匹配
            if white_pixels > 0.9 * (scaled_w * scaled_h) or black_pixels > 0.9 * (scaled_w * scaled_h):
                print(f"⚠️ 匹配区域异常 (可能误匹配)")
                return False
                
            # 点击图标
            self.driver.tap([(center_x, center_y)], duration)
            print(f"✅ 找到并点击图标 (置信度: {max_val:.2f}, 缩放: {scale:.2f}) 位置: ({center_x}, {center_y})")
            return True
                
        except Exception as e:
            print(f"❌ 图标识别失败: {str(e)}")
            return False


    def get_snapshot(self, file_path=None, compare=None, threshold=0.7, page_name="test"):
        max_retries = 3
        retry_delay = 1  # 秒
        
        for attempt in range(max_retries):
            try:
                # 获取当前屏幕截图
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_np = np.frombuffer(screenshot, np.uint8)
                screen = cv2.imdecode(screenshot_np, cv2.IMREAD_COLOR)
                
                # 添加连接重置检查
                if screen is None or screen.size == 0:
                    raise Exception("获取的截图为空")
                    
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
                    template = cv2.imread(file_path, cv2.IMREAD_COLOR)
                    if template is None:
                        print(f"❌ 无法加载{page_name}模板图像")
                        return False
            
                    # 进行模板匹配
                    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
                    if max_val >= threshold:
                        print(f"✅ 通过图像匹配点击{page_name}按钮 (置信度: {max_val:.2f})")
                        time.sleep(1)
                        return True
                    else:
                        print(f"❌ 未找到匹配的{page_name}按钮 (最高置信度: {max_val:.2f})")
                else:
                    print('compare is None')
                    return 'compare is None'
            
                return False
            
            except Exception as e:
                print(f"⚠️ 截图失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    return False
                
                # 检查特定错误类型
                if "instrumentation process is not running" in str(e) or "socket hang up" in str(e):
                    try:
                        # 尝试重启driver连接
                        capabilities = getattr(self.driver, '_caps', {})
                        server_url = getattr(self.driver, 'command_executor', None)
                        if server_url is None:
                            print("❌ 无法获取Appium服务器URL")
                            return False
                            
                        # 确保server_url是字符串类型
                        if hasattr(server_url, '_url'):
                            server_url_str = str(server_url._url)
                        else:
                            server_url_str = str(server_url)
                        
                        # 清理URL中的控制字符
                        server_url_str = ''.join(char for char in server_url_str if ord(char) >= 32)
                        
                        # 关闭旧的driver
                        try:
                            self.driver.quit()
                        except:
                            pass
                            
                        # 创建新的driver连接
                        try:
                            capabilities['newCommandTimeout'] = 600  # 设置为10分钟
                            
                            self.driver = webdriver.Remote(
                                command_executor=server_url_str,
                                options=UiAutomator2Options().load_capabilities(capabilities)
                            )
                        except Exception as e:
                            print(f"❌ 恢复连接失败: {str(e)}")
                            return False
                        print("🔄 已重新建立Appium连接")
                        time.sleep(3)  # 等待更长时间让服务稳定
                    except Exception as restart_error:
                        print(f"❌ 恢复连接失败: {str(restart_error)}")
                        return False
                
                # 增加重试延迟时间，指数退避
                time.sleep(retry_delay * (attempt + 1))
                # 尝试重置driver连接
                try:
                    self.driver.reset()
                except:
                    pass


    def coordinates(self, width, height, input_text=None, press_keycode=None):
        try:
            if not self.driver:
                print("⚠️ 错误: driver未初始化")
                return False
    
            # 直接使用缓存的窗口尺寸，避免重复获取
            x = self.window_size['width'] * width
            y = self.window_size['height'] * height
            
            # 简化重试逻辑
            try:
                self.driver.tap([(x, y)], 0)  # 减少点击持续时间
                print(f"📍 已通过坐标 ({x}, {y})点击")
            except Exception as e:
                print(f"❌ 坐标点击失败: {str(e)}")
                return False
    
            if input_text is not None and press_keycode is not None:
                try:
                    self.driver.execute_script('mobile: type', {'text': input_text})
                    self.driver.press_keycode(press_keycode)
                    print(f"📍 已通过坐标 ({x}, {y})输入{input_text}内容")
                except Exception as e:
                    print(f"❌ 输入文本失败: {str(e)}")
                    return False
                
            return True
        except Exception as e:
            print(f"❌ 坐标点击失败: {str(e)}")
            return False




    # 返回点击主城
    def Page_Percent(self, num=10, x_percent=0.07, y_percent=0.96):
        """按屏幕百分比点击"""
        try:
            for i in range(num):
                if i == 0:
                    self.coordinates(width=0.035, height=0.95)
                is_home = self.get_snapshot(file_path="../page_png/home.png", compare=True, page_name="主城")
                if is_home is True:
                    # 如果在首页则返回True
                    return True
                elif i == 5 or i == 9:
                    self.coordinates(width=0.835, height=0.345)
                elif i == 3:
                    self.coordinates(width=0.92, height=0.2)
                else:
                    self.coordinates(width=x_percent, height=y_percent)
            return False
        except Exception as e:
            print(e)
            return False



    def is_Vip_Page(self):
        pass
    def is_GoodFriend_Page(self):
        pass
    def is_Chat_Page(self):
        pass
    def is_Arena_Page(self):
        pass
    def is_Trials_Tower_Page(self):
        pass
    def is_Recruit_Page(self):
        pass
    def is_Store_Page(self):
        pass
    def is_Legion_Page(self):
        pass
    def is_OutDoors_Page(self):
        pass
    def is_Campaign_Page(self):
        pass
    def is_Task_Page(self):
        pass




