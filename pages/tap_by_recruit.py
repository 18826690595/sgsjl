


import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Recruit:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()
        self.tap_by_percent = Tap_By_Percent()


    # 名将招募
    def Page_Recruit(self, duration=300):
        # 初始化点击主城
        self.tap_by_Recruit(5)
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



# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Recruit()
    test.Page_Recruit()