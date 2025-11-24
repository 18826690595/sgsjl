import pytesseract
import cv2
import numpy as np
from PIL import Image
import pyautogui  # 新增导入

# 获取当前屏幕截图
screenshot = pyautogui.screenshot()
image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 图像预处理优化
# 1. 二值化
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# 2. 降噪优化
kernel = np.ones((1, 1), np.uint8)  # 减小核大小避免过度腐蚀
processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
# 3. 锐化优化
processed = cv2.filter2D(processed, -1, np.array([[0,-1,0], [-1,5,-1], [0,-1,0]]))

# 使用pytesseract获取文字位置信息 - 配置优化
config = '--psm 6 --oem 3 -c preserve_interword_spaces=1'  # 移除了白名单限制
data = pytesseract.image_to_data(
    processed, 
    lang='chi_sim+eng',  # 添加英文支持
    output_type=pytesseract.Output.DICT,
    config=config
)

# 打印所有识别结果
print("完整识别结果:")
for i in range(len(data['text'])):
    if data['text'][i].strip():  # 只打印非空文本
        print(f"文本: '{data['text'][i]}', 位置: ({data['left'][i]}, {data['top'][i]}), 大小: {data['width'][i]}x{data['height'][i]}")

# 查找"进入游戏"文字位置
target_text = "命"
target_chars = list(target_text)  # 拆分为单个字符
found_chars = []
tolerance = 5  # y坐标容差范围

# 第一次遍历：收集所有匹配字符
for i, text in enumerate(data['text']):
    text = text.strip()
    print(f"识别到的文本: '{text}'")  # 添加这行打印所有识别到的文本
    if text in target_chars:  # 检查是否是目标字符之一
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        found_chars.append({
            'char': text,
            'x': x,
            'y': y,
            'w': w,
            'h': h
        })

# 第二次遍历：找出同一高度的四个字符
if len(found_chars) >= 4:
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
            y_key = char['y']
        if y_key not in y_groups:
            y_groups[y_key] = []
        y_groups[y_key].append(char)
    
    # 找出包含四个字符的组
    for y_val, chars in y_groups.items():
        if len(chars) == 4:
            # 按x坐标排序
            sorted_chars = sorted(chars, key=lambda c: c['x'])
            # 计算整体中心坐标
            min_x = min(c['x'] for c in sorted_chars)
            max_x = max(c['x'] + c['w'] for c in sorted_chars)
            min_y = min(c['y'] for c in sorted_chars)
            max_y = max(c['y'] + c['h'] for c in sorted_chars)
            center_x = (min_x + max_x) // 2
            center_y = (min_y + max_y) // 2
            print(f"找到'进入游戏'，中心坐标: ({center_x}, {center_y})")
            break
    else:
        print("未找到同一高度的四个目标字符")
else:
    print("未找到足够的目标字符")



