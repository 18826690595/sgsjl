import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_VIP:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()
        self.tap_by_percent = Tap_By_Percent()

    # 领取vip经验
    def Page_Vip(self, duration=10):
        """按屏幕百分比点击"""
        # window_size = self.driver.get_window_size()
        # 点击主城
        self.tap_by_percent.Page_Percent(5)
        page_name = "../page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:

            # 点击vip入口
            self.utils.coordinates(width=0.07, height=0.1)

            # x = window_size['width'] * 0.07
            # y = window_size['height'] * 0.1
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) vip入口")
            # time.sleep(1)

            # 点击宝箱
            self.utils.coordinates(width=0.94, height=0.24)

            # x = window_size['width'] * 0.94
            # y = window_size['height'] * 0.24
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) 宝箱")
            # time.sleep(1)

            # 点击领取
            self.utils.coordinates(width=0.5, height=0.58)

            # x = window_size['width'] * 0.5
            # y = window_size['height'] * 0.58
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) 点击领取按钮")
            # time.sleep(1)

            print("vip经验已领取")
            return True
        else:
            print("流程异常跳过vip任务...")
            return False




# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_VIP()
    test.Page_Vip()