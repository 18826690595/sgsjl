


import time

from sgmjl.core.utils import Utils


class Tap_By_Recruit:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()


    # 名将招募
    def Page_Recruit(self, duration=300):
        # 初始化点击主城
        self.utils.Page_Percent(5)
        page_name = "../page_png/home.png"
        is_home = self.utils.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            # 点击招募入口
            self.utils.coordinates(width=0.6, height = 0.5)

            # 获取招募页面截图

            # 点击招募
            time.sleep(0.5)
            self.utils.coordinates(width=0.23, height = 0.72)

            # 返回首页
            self.utils.Page_Percent(20)
        else:
            print("名将招募异常")



# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Recruit()
    test.Page_Recruit()