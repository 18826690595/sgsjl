import time

from core.utils import Utils


class Tap_By_Good_Friend(Utils):

    def __init__(self, driver):
        super().__init__(driver)


    # 好友日常任务
    def Page_good_friend(self):
        """按屏幕百分比点击"""
        # 点击主城
        is_home = self.Page_Percent()
        if is_home is True:
            # 点击好友入口
            self.coordinates(width=0.07, height=0.78)
            time.sleep(1)

            # 点击好友列表
            self.coordinates(width=0.89, height=0.95)
            time.sleep(0.5)

            # 点击一键收送
            self.coordinates(width=0.83, height=0.85)
            # time.sleep(1)

            # 好友切磋
            self.coordinates(width=0.12, height=0.22)
            time.sleep(0.5)
            self.click_icon("../page_png/PK_icon.png")
            # 点击出战
            time.sleep(1)
            self.coordinates(width=0.66, height=0.85)

            time.sleep(1.3)
            self.coordinates(width=0.95, height=0.84)

            time.sleep(2)
            self.coordinates(width=0.25, height=0.87)

        else:
            print("好友流程异常跳过")
