import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Store:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()


    # 商店
    def Page_Store(self, duration=300):
        # 初始化点击主城
        self.utils.Page_Percent(5)
        page_name = "../page_png/home.png"
        is_home = self.utils.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            # 点击商店入口
            time.sleep(0.5)
            self.utils.coordinates(width=0.96, height=0.59)
            time.sleep(0.5)
            self.utils.coordinates(width=0.26, height = 0.5)

            time.sleep(0.5)
            self.utils.coordinates(width=0.75, height = 0.68)

            time.sleep(0.5)
            self.utils.coordinates(width=0.5, height = 0.5)

            time.sleep(0.5)
            self.utils.coordinates(width=0.75, height = 0.68)
        else:
            print("商店流程异常")

# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Store()
    test.Page_Store()