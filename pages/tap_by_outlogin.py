import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_OutLogin:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()


    # 退出登录
    def Page_Out_Login(self, duration=1000):
        """按屏幕百分比点击"""

        # 点击主城
        self.utils.Page_Percent(5)
        is_home = self.utils.get_snapshot(file_path="../page_png/home.png", compare=True)
        if is_home is True:
            # 点击头像
            self.utils.coordinates(width=0.07, height = 0.05)
            time.sleep(1)
            is_home = self.utils.get_snapshot(file_path="../page_png/Settings.png", compare=True)
            if is_home is True:
                # 点击设置
                self.utils.coordinates(width=0.92, height=0.85)
                time.sleep(1)

                # 点击退出登录
                self.utils.coordinates(width=0.5, height=0.63)
                time.sleep(1)
            else:
                print("未找到设置按钮")
        else:
            print("退出登录流程异常")
            return False

# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_OutLogin()
    test.Page_Out_Login()