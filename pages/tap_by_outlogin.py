import time

from core.utils import Utils

class Tap_By_OutLogin:

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)



    # 退出登录
    def Page_Out_Login(self):
        """按屏幕百分比点击"""

        # 点击主城
        is_home = self.utils.Page_Percent()
        if is_home is True:
            # 点击头像
            self.utils.coordinates(width=0.07, height = 0.05)
            time.sleep(1)
            # is_Settings = self.utils.get_snapshot(file_path="../page_png/Settings.png", compare=True, threshold=0.5)
            # if is_Settings is True:
            # 点击设置
            self.utils.coordinates(width=0.92, height=0.85)
            time.sleep(1)

            # 点击退出登录
            self.utils.coordinates(width=0.5, height=0.63)
        else:
            print("退出登录流程异常")
            return False
        time.sleep(3)

