import time

from core.utils import Utils


class Tap_By_Task(Utils):

    def __init__(self, driver):
        super().__init__(driver)



    # 完成任务
    def Page_Task(self):
        # 初始化点击主城
        is_home = self.Page_Percent()
        if is_home is True:
            # 点击任务入口
            time.sleep(0.5)
            self.coordinates(width=0.95, height=0.72)
            time.sleep(1)
            self.coordinates(width=0.5, height=0.88)

