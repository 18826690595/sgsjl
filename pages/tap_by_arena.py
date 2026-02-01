import time

from core.utils import Utils


class Tap_By_Arena:

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)

    # 竞技场
    def Page_Arena(self):
        # 点击主城
        self.utils.Page_Percent()
        # 判断是否在首页
        is_home = self.utils.Page_Percent()
        if is_home is True:
            # 点击擂台入口
            print("点击擂台入口")
            self.utils.coordinates(width=0.2, height=0.5)
            time.sleep(1)
            # 点击竞技场入口
            self.utils.coordinates(width=0.2, height=0.2)
            time.sleep(0.5)
            self.utils.coordinates(width=0.5, height=0.86)
            # 修正错误的坐标值
            self.utils.coordinates(width=0.5, height=0.78)  # 原为 height=78

            for i in range(5):
                time.sleep(1)
                self.utils.coordinates(width=0.73, height=0.53)
                self.utils.coordinates(width=0.73, height=0.56)
                time.sleep(1.5)
                self.utils.coordinates(width=0.7, height=0.88)

            time.sleep(0.5)
            self.utils.coordinates(width=0.7, height=0.88)

        else:
            print("竞技场流程异常")

