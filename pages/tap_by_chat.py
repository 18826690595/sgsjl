import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Chat:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()


    # 聊天、军团
    def Page_Chat(self, text="1"):
        """按屏幕百分比点击"""
        # 点击主城
        self.utils.Page_Percent(5)
        is_home = self.utils.get_snapshot(file_path="../page_png/home.png", compare=True)
        if is_home is True:
            # 点击聊天入口
            self.utils.coordinates(width=0.07, height=0.82)
            time.sleep(1)

            # 点击世界
            self.utils.coordinates(width=0.07, height=0.25)
            time.sleep(1)

            # 聊天输入框
            self.utils.coordinates(width=0.3, height=0.9)
            time.sleep(1)
            # 输入文本
            self.utils.coordinates(width=0.3, height=0.9, input_text=text, press_keycode=66)
            # self.driver.press_keycode(66)  # 66是回车键的keycode
            time.sleep(0.5)

            # 点击发送消息
            self.utils.coordinates(width=0.8, height=0.9)
            time.sleep(1)

            # 点击军团
            self.utils.coordinates(width=0.07, height=0.3)
            time.sleep(1)

            # 点击求助
            self.utils.coordinates(width=0.68, height=0.83)
            time.sleep(1)

            # 点击英雄碎片
            self.utils.coordinates(width=0.23, height=0.36)
            time.sleep(1)

            # 点击元宝
            self.utils.coordinates(width=0.8, height=0.5)
            time.sleep(1)

            # 点击发布求助
            self.utils.coordinates(width=0.5, height=0.7)
            time.sleep(1)

            # 点击军团援助
            self.utils.coordinates(width=0.83, height=0.83)
            time.sleep(1)

            # 点击帮助
            for i in range(5):
                self.utils.coordinates(width=0.78, height=0.3)

            return True

        else:
            print("军团援助异常pass")
            return False

# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Chat()
    test.Page_Chat()