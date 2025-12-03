import time

from core.utils import Utils
from pages.tap_by_percent import Tap_By_Percent


class Tap_By_Task:

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)



    # 完成任务
    def Page_Task(self, duration=300):
        # 初始化点击主城
        is_home = self.utils.Page_Percent(5)
        if is_home is True:
            # 点击任务入口
            time.sleep(0.5)
            self.utils.coordinates(width=0.95, height=0.72)
            time.sleep(1)
            page_name = "../page_png/daily_tasks.png"
            daily_tasks = self.utils.get_snapshot(file_path=page_name, compare=True, threshold=0.7, page_name="日常任务页面")
            if daily_tasks is True:
                self.utils.coordinates(width=0.5, height=0.88)
                print(f"📍 已通过坐标点击一键领取任务奖励")
