import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Good_Friend:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()
        self.tap_by_percent = Tap_By_Percent()


    # 好友日常任务
    def Page_good_friend(self, duration=300, task_test="任务已完成"):
        """按屏幕百分比点击"""
        window_size = self.driver.get_window_size()
        # 点击主城
        self.tap_by_percent(5)
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            # 点击好友入口
            x = window_size['width'] * 0.07
            y = window_size['height'] * 0.78
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击好友入口")
            time.sleep(1)

            # 点击好友列表
            x = window_size['width'] * 0.89
            y = window_size['height'] * 0.95
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击好友列表")
            time.sleep(1)

            # 点击一键收送
            x = window_size['width'] * 0.83
            y = window_size['height'] * 0.85
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标({x:.0f}, {y:.0f}) 点击一键收送")
            time.sleep(1)

            return task_test
        else:
            print("好友流程异常跳过")
# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Good_Friend()
    test.Page_good_friend()