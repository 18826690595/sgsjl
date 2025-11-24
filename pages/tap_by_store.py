import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Store:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()
        self.tap_by_percent = Tap_By_Percent()


    # 商店
    def Page_Store(self, duration=300):
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

# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Store()
    test.Page_Store()