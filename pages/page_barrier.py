import time

from core.utils import Utils


class Page_Barrier():

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)


    # 推图
    def page_barrier(self):
        # 初始化点击主城
        is_home = self.utils.Page_Percent(5)
        if is_home is True:
            self.utils.coordinates(width=0.93, height=0.96)

        i = 0
        while True:
            # 点击挑战
            time.sleep(1)
            self.utils.coordinates(width=0.5, height=0.85)

            # 点击出战
            time.sleep(1)
            self.utils.coordinates(width=0.66, height=0.85)

            time.sleep(1.3)
            self.utils.coordinates(width=0.95, height=0.84)

            time.sleep(2)
            self.utils.coordinates(width=0.75, height=0.88)

            i = i + 1
            if i == 20:
                break




