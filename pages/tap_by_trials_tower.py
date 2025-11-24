import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Trials_Tower:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()
        self.tap_by_percent = Tap_By_Percent()

    # 斗塔
    def Page_Trials_Tower(self, duration=300):
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


# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Trials_Tower()
    test.Page_Trials_Tower()