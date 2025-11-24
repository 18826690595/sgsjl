import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Arena:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()  # 将driver传递给Locators类
        self.tap_by_percent = Tap_By_Percent()

    # 竞技场
    def Page_Arena(self, duration=300):
        window_size = self.driver.get_window_size()
        # 点击主城
        self.tap_by_percent(5)
        # 判断是否在首页
        page_name = "../page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:

            # 初始化点击主城
            self.tap_by_percent(5)

            # 点击擂台入口
            # print("\n🔄 点击同意服务条款...")
            # x = window_size['width'] * 0.2
            # y = window_size['height'] * 0.5
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x}, {y})点击擂台入口")
            self.utils.coordinates(width=0.2, height=0.5)
            time.sleep(1)
            # 点击竞技场入口
            # x = window_size['width'] * 0.2
            # y = window_size['height'] * 0.2
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x}, {y})点击竞技场入口")
            self.utils.coordinates(width=0.2, height=0.2)
            time.sleep(0.5)
            # x = window_size['width'] * 0.5
            # y = window_size['height'] * 0.86
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x}, {y})点击挑战")
            self.utils.coordinates(width=0.5, height=0.86)

            # x = window_size['width'] * 0.5
            # y = window_size['height'] * 0.78
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x}, {y})点击刷新对手")
            self.utils.coordinates(width=0.5, height=78)

            for i in range(5):
                time.sleep(1)
                # x = window_size['width'] * 0.72
                # y = window_size['height'] * 0.52
                # self.driver.tap([(x, y)], duration)
                # print(f"📍 已通过坐标 ({x}, {y})点击挑战对手")
                self.utils.coordinates(width=0.72, height=0.52)
                time.sleep(1.5)
                # x = window_size['width'] * 0.7
                # y = window_size['height'] * 0.88
                # self.driver.tap([(x, y)], duration)
                # print(f"📍 已通过坐标 ({x}, {y})点击返回玩法")
                self.utils.coordinates(width=0.7, height=0.88)

        else:
            print("竞技场流程异常")


# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Arena()
    test.Page_Arena()