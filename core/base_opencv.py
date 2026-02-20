import cv2
import numpy as np
from .base_app import AppAutoManager

class OpenCVTemplateMatcher(AppAutoManager):  # 继承 AppAutoManager
    def __init__(self):
        super().__init__()  # 调用父类初始化

    def get_snapshot(self, driver):
        
        # 获取当前屏幕截图
        screenshot = driver.get_screenshot_as_png()
        screenshot_np = np.frombuffer(screenshot, np.uint8)
        screen = cv2.imdecode(screenshot_np, cv2.IMREAD_COLOR)
        return screen
                






    def match_and_click(self, template_path, region, threshold=0.8, is_click=False):
        """
        截取指定区域进行图像比对，匹配成功后点击模板中心位置
        :param template_path: 模板图片路径
        :param region: 指定区域 (x1, y1, x2, y2)
        :param threshold: 匹配阈值，默认0.8
        :return: 是否匹配并点击成功
        """
        # 读取模板图片
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            raise ValueError(f"无法读取模板图片: {template_path}")
        
        # 获取屏幕截图
        screen = self.get_snapshot(self.driver)  # 使用继承的driver属性
        
        # 裁剪指定区域
        x1, y1, x2, y2 = region
        screen = screen[y1:y2, x1:x2]
        
        # 进行模板匹配
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        print(max_val)
        if max_val < threshold:
            return False
        
        if is_click == True:
            # 计算按钮中心位置并点击
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2 + x1
            center_y = max_loc[1] + h // 2 + y1
            
            # 使用ActionChains点击
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)  # 使用继承的driver属性
            actions.move_by_offset(center_x, center_y).click().perform()
        
        return True


    
    def OpenCV_add(self, template_path, region=None, driver=None):
        """
        在指定区域内匹配模板按钮
        :param template_path: 模板图片路径
        :param region: 指定区域 (x1, y1, x2, y2)，不传则全屏匹配
        :return: 匹配成功返回按钮中心位置(x,y)百分比坐标，否则返回None
        """
        # 读取模板图片
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            raise ValueError(f"无法读取模板图片: {template_path}")
        
        # 获取屏幕截图
        screen = self.get_snapshot(driver)
        
        # 如果指定了区域，则裁剪屏幕图像
        if region:
            x1, y1, x2, y2 = region
            screen = screen[y1:y2, x1:x2]
        
        # 进行模板匹配
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        # 设置匹配阈值(可根据实际情况调整)
        threshold = 0.8
        if max_val < threshold:
            return None
        
        # 计算按钮中心位置
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        
        # 如果指定了区域，需要加上偏移量
        if region:
            x1, y1, _, _ = region
            center_x += x1
            center_y += y1
        
        # 转换为百分比坐标
        screen_h, screen_w = screen.shape[:2]
        percent_x = round(center_x / screen_w * 100, 2)
        percent_y = round(center_y / screen_h * 100, 2)
        
        return (percent_x, percent_y)
    
