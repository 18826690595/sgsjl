import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Chat:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()
        self.tap_by_percent = Tap_By_Percent()


    # 聊天、军团
    def Page_Chat(self, duration=300, task_test="任务已完成", text="t"):
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

# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Chat()
    test.Page_Chat()