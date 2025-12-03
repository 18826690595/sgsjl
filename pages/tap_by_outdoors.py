
import time

from core.utils import Utils



class Tap_By_OutDoors:

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)




    # 野外
    def Page_OutDoors(self, duration=300):
        # 初始化点击主城
        is_home = self.utils.Page_Percent(5)
        if is_home is True:
            time.sleep(0.5)
            self.utils.coordinates(width=0.76, height = 0.94)

            time.sleep(0.5)
            self.utils.coordinates(width=0.3, height = 0.5)

            time.sleep(0.5)
            self.utils.coordinates(width=0.9, height = 0.7)

            time.sleep(0.5)
            self.utils.coordinates(width=0.5, height = 0.65)

            # 点击返回按钮
            # self.tap_by_percent()
            for i in range(2):
                self.utils.coordinates(width=0.07, height = 0.96)
                time.sleep(0.5)

                is_outdoors1 = self.utils.get_snapshot(file_path="../page_png/outdoors1.png", compare=True)
                if is_outdoors1 is True:
                    time.sleep(0.5)
                    self.utils.coordinates(width=0.3, height=0.2)

                    time.sleep(0.5)
                    self.utils.coordinates(width=0.55, height=0.93)
                    time.sleep(0.5)

                    # 循环扫荡3次
                    for i in range(6):
                        time.sleep(0.5)
                        self.utils.coordinates(width=0.85, height=0.45)

                        outdoors = self.utils.get_snapshot(file_path="../page_png/fuben_saodang_tishi.png", compare=True, threshold=0.5)
                        if outdoors is True:
                            time.sleep(0.5)
                            self.utils.coordinates(width=0.7, height=0.60)
                        time.sleep(0.5)
                        # self.tap_by_percent()
                        self.utils.coordinates(width=0.07, height=0.96)

        elif is_home is False:
            print("副本页面不匹配")
        else:
            print("未知错误")

