import time

from sgmjl.core.utils import Utils


class Tap_By_Good_Friend:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()


    # 好友日常任务
    def Page_good_friend(self):
        """按屏幕百分比点击"""
        # 点击主城
        self.utils.Page_Percent(5)
        page_name = "../page_png/home.png"
        is_home = self.utils.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            # 点击好友入口
            self.utils.coordinates(width=0.07, height=0.78)
            time.sleep(1)

            # 点击好友列表
            self.utils.coordinates(width=0.89, height=0.95)
            time.sleep(1)

            # 点击一键收送
            self.utils.coordinates(width=0.83, height=0.85)
            time.sleep(1)

            return True
        else:
            print("好友流程异常跳过")
# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Good_Friend()
    test.Page_good_friend()