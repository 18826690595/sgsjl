import time

from sgmjl.core.utils import Utils


class Tap_By_Percent:

    def __init__(self, driver=None):
        self.driver = driver
        self.coordinates = Utils()

    # 返回点击主城
    def Page_Percent(self, num=1, x_percent=0.07, y_percent=0.96, duration=300, desc="返回主城"):
        """按屏幕百分比点击"""
        for i in range(num):
            self.coordinates.coordinates(width=x_percent, height=y_percent)
            time.sleep(0.5)

            # window_size = self.driver.get_window_size()
            # x = window_size['width'] * x_percent
            # y = window_size['height'] * y_percent
            # for i in range(num):
            #     self.driver.tap([(x, y)], duration)
            #     print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) {desc}")
            #     time.sleep(0.5)
            # return x, y

# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Percent()
    test.Page_Percent()