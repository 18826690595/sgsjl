import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Legion:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()
        self.tap_by_percent = Tap_By_Percent()


    # 军团
    def Page_Legion(self, duration=300):
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


# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Legion()
    test.Page_Legion()