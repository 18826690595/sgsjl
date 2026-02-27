import time

from core.utils import Utils


class Tap_By_VIP(Utils):

    def __init__(self, driver):
        super().__init__(driver)
        
    # 领取vip经验
    def Page_Vip(self):
        """按屏幕百分比点击"""
        # 点击主城
        is_home = self.Page_Percent()
        try:
            if is_home is True:  # 修复条件判断
                try:
                    # 点击vip入口
                    self.coordinates(width=0.07, height=0.1)
                    # 点击宝箱
                    self.coordinates(width=0.94, height=0.24)
                    # 点击领取
                    time.sleep(0.5)
                    self.coordinates(width=0.5, height=0.58)

                    print("vip经验已领取")
                    return True
                except Exception as e:
                    print(f"执行vip任务时出错: {str(e)}")
                    # 可以添加driver重启逻辑
                    return False
        except Exception as e:
            print(f"执行流程时出错: {str(e)}")
            return False



