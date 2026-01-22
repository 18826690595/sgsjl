import time

from core.utils import Utils

class Tap_By_Recruit:
    
    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)


    # 名将招募
    def Page_Recruit(self):
        # 初始化点击主城
        is_home = self.utils.Page_Percent()
        if is_home is True:
            # 点击招募入口
            self.utils.coordinates(width=0.6, height = 0.5)

            # 获取招募页面截图
            time.sleep(0.5)
            self.utils.coordinates(width=0.8, height=0.67)
            # 点击招募
            time.sleep(0.5)
            self.utils.coordinates(width=0.23, height = 0.72)
            # 去除判断招募成功
            # is_zhaomu_chenggong = self.utils.get_snapshot(file_path="../page_png/zhaomu_chenggong.png", compare=True, page_name="招募成功")
            # if is_zhaomu_chenggong is True:
            #     self.utils.coordinates(width=0.1, height = 0.87)
            #     return True
            # 返回首页
            self.utils.Page_Percent(20)
        else:
            print("名将招募异常")



