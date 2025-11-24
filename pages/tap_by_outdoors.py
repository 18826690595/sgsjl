
import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_OutDoors:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()
        self.tap_by_percent = Tap_By_Percent()




    # 野外
    def Page_OutDoors(self, duration=300):
        window_size = self.driver.get_window_size()
        # 初始化点击主城
        self.tap_by_percent(3)
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            time.sleep(0.5)
            x = window_size['width'] * 0.76
            y = window_size['height'] * 0.94
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击野外入口")

            time.sleep(0.5)
            x = window_size['width'] * 0.3
            y = window_size['height'] * 0.5
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击火烧赤壁入口")

            time.sleep(0.5)
            x = window_size['width'] * 0.9
            y = window_size['height'] * 0.7
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击一键扫荡入口")

            time.sleep(0.5)
            x = window_size['width'] * 0.5
            y = window_size['height'] * 0.65
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击扫荡")

            # 点击返回按钮
            self.tap_by_percent()

            page_name = "./page_png/outdoors1.png"
            outdoors = self.get_snapshot(file_path=page_name, compare=True)
            if outdoors is True:
                time.sleep(0.5)
                x = window_size['width'] * 0.3
                y = window_size['height'] * 0.2
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x}, {y})点击副本入口")

                # button_name = "扫荡"
                # self.find_game_entry(button_name)

                time.sleep(0.5)
                x = window_size['width'] * 0.55
                y = window_size['height'] * 0.93
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标 ({x}, {y})点击装备副本入口")
                time.sleep(0.5)

                for i in range(3):
                    time.sleep(0.5)
                    x = window_size['width'] * 0.85
                    y = window_size['height'] * 0.45
                    self.driver.tap([(x, y)], 0)
                    print(f"📍 已通过坐标 ({x}, {y})点击扫荡")

                    page_name = "./page_png/fuben_saodang_tishi.png"
                    outdoors = self.get_snapshot(file_path=page_name, compare=True, threshold=0.5)
                    if outdoors is True:
                        time.sleep(0.5)
                        x = window_size['width'] * 0.7
                        y = window_size['height'] * 0.60
                        self.driver.tap([(x, y)], 10)
                        print(f"📍 已通过坐标 ({x}, {y})点击扫荡")

                    time.sleep(0.5)
                    self.tap_by_percent()

        elif is_home is False:
            print("副本页面不匹配")
        else:
            print("未知错误")


# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_OutDoors()
    test.Page_OutDoors()