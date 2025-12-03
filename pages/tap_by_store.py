import time

from core.utils import Utils


class Tap_By_Store:

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)


    # 商店
    def Page_Store(self):
        # 初始化点击主城
        is_home = self.utils.Page_Percent(5)
        if is_home is True:
            # 点击商店入口
            time.sleep(0.5)
            self.utils.coordinates(width=0.96, height=0.59)
            time.sleep(0.5)
            self.utils.coordinates(width=0.26, height = 0.5)

            time.sleep(0.5)
            self.utils.coordinates(width=0.75, height = 0.68)

            time.sleep(0.5)
            self.utils.coordinates(width=0.5, height = 0.5)

            time.sleep(0.5)
            self.utils.coordinates(width=0.75, height = 0.68)
        else:
            print("商店流程异常")

