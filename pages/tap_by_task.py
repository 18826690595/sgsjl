import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Task:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()
        self.tap_by_percent = Tap_By_Percent()



    # 完成任务
    def Page_Task(self, duration=300):
        # 初始化点击主城
        self.tap_by_percent(5)
        window_size = self.driver.get_window_size()
        # 点击任务入口
        time.sleep(0.5)
        x = window_size['width'] * 0.95
        y = window_size['height'] * 0.72
        self.driver.tap([(x, y)], duration)
        print(f"📍 已通过坐标 ({x}, {y})点击任务入口")
        time.sleep(1)
        page_name = "./page_png/daily_tasks.png"
        daily_tasks = self.get_snapshot(file_path=page_name, compare=True, threshold=0.7, page_name="日常任务页面")
        if daily_tasks is True:
            x = window_size['width'] * 0.5
            y = window_size['height'] * 0.88
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标 ({x}, {y})点击一键领取任务奖励")

# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Task()
    test.Page_Task()