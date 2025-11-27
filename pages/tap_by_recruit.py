


import time

from sgmjl.core.utils import Utils

class Tap_By_Recruit:
    _driver = None  # 类变量保存driver实例
    
    def __init__(self, driver=None):
        if Tap_By_Recruit._driver is None:
            if driver is None:
                # 这里应该初始化driver
                # Tap_By_Recruit._driver = 你的driver初始化代码
                pass
            else:
                Tap_By_Recruit._driver = driver
        self.driver = Tap_By_Recruit._driver
        self.utils = Utils()


    # 名将招募
    def Page_Recruit(self, duration=300):
        # 初始化点击主城
        self.utils.Page_Percent(5)
        is_home = self.utils.get_snapshot(file_path="../page_png/home.png", compare=True)
        if is_home is True:
            # 点击招募入口
            self.utils.coordinates(width=0.6, height = 0.5)

            # 获取招募页面截图

            # 点击招募
            time.sleep(0.5)
            self.utils.coordinates(width=0.23, height = 0.72)
            zhaomu_chenggong = self.utils.get_snapshot(file_path="../page_png/zhaomu_chenggong.png", compare=True, page_name="招募成功")
            if zhaomu_chenggong is True:
                self.utils.coordinates(width=0.1, height = 0.87)
            # 返回首页
            self.utils.Page_Percent(20)
        else:
            print("名将招募异常")



# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Recruit()
    test.Page_Recruit()