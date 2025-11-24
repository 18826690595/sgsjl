import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_OutLogin:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()
        self.tap_by_percent = Tap_By_Percent()


    # 退出登录
    def Page_Out_Login(self, duration=1000):
        """按屏幕百分比点击"""

        window_size = self.driver.get_window_size()

        # 点击主城
        self.tap_by_percent(5)
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:

            # 点击头像
            x = window_size['width'] * 0.07
            y = window_size['height'] * 0.05
            self.driver.tap([(x, y)], duration)
            print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) 点击头像")
            time.sleep(1)
            page_name = "./page_png/Settings.png"
            is_home = self.get_snapshot(file_path=page_name, compare=True)
            if is_home is True:
                # 点击设置
                x = window_size['width'] * 0.92
                y = window_size['height'] * 0.85
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) 设置")
                time.sleep(1)

                # 点击退出登录
                x = window_size['width'] * 0.5
                y = window_size['height'] * 0.63
                self.driver.tap([(x, y)], duration)
                print(f"📍 已通过坐标点击 ({x:.0f}, {y:.0f}) 点击退出登录按钮")
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