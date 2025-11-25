import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_VIP():

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()

    # 领取vip经验
    def Page_Vip(self):
        """按屏幕百分比点击"""
        # 点击主城
        is_home = self.utils.Page_Percent(5)
        try:
            if is_home:  # 修复条件判断
                try:
                    # 点击vip入口
                    self.utils.coordinates(width=0.07, height=0.1)
                    # 点击宝箱
                    self.utils.coordinates(width=0.94, height=0.24)
                    # 点击领取
                    self.utils.coordinates(width=0.5, height=0.58)

                    print("vip经验已领取")
                    return True
                except Exception as e:
                    print(f"执行vip任务时出错: {str(e)}")
                    # 可以添加driver重启逻辑
                    return False
        except Exception as e:
            print(f"执行流程时出错: {str(e)}")
            return False




# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_VIP()
    test.Page_Vip()