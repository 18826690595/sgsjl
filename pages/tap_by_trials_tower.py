import time

from core.utils import Utils


class Tap_By_Trials_Tower:

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)


    # 斗塔
    def Page_Trials_Tower(self):
        # window_size = self.driver.get_window_size()
        # 初始化点击主城
        is_home = self.utils.Page_Percent(5)
        if is_home is True:
            # 点击斗塔入口
            self.utils.coordinates(width=0.4, height=0.5)
            for i in range(3):
                # 点击挑战
                time.sleep(1)
                self.utils.coordinates(width=0.5, height=0.85)

                # 点击出战
                time.sleep(1)
                self.utils.coordinates(width=0.66, height=0.85)

                time.sleep(1.3)
                self.utils.coordinates(width=0.95, height=0.84)

                time.sleep(2)
                self.utils.coordinates(width=0.25, height=0.87)
            # 点击每日奖励
            self.utils.coordinates(width=0.95, height=0.3)
            time.sleep(0.5)
            # 点击领取
            self.utils.coordinates(width=0.5, height=0.8)

        else:
            print("斗塔流程异常")


# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Trials_Tower()
    test.Page_Trials_Tower()