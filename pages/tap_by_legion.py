import time

from core.utils import Utils


class Tap_By_Legion(Utils):

    def __init__(self, driver):
        super().__init__(driver)


    # 军团
    def Page_Legion(self):
        # 初始化点击主城
        is_home = self.Page_Percent()
        if is_home is True:
            # 点击军团入口
            self.coordinates(width=0.58, height=0.96)
            time.sleep(0.5)

            is_lianmeng = self.get_snapshot(file_path="../page_png/lianmeng.png", compare=True)
            if is_lianmeng is True:
                # 点击军团、联盟入口
                self.coordinates(width=0.5, height=0.2)
                time.sleep(0.5)

            # 点击祭祀入口
            self.coordinates(width=0.36, height=0.72)
            time.sleep(0.5)
            # 点击祭祀
            self.coordinates(width=0.5, height=0.78)
            time.sleep(0.5)
            # 点击祭祀确定
            self.coordinates(width=0.7, height=0.6)
            # time.sleep(1)

            for i in range(2):
                # 点击关闭祭祀页面
                print("点击关闭祭祀页面")
                self.coordinates(width=0.91, height=0.19)

            # 点击军团副本入口
            self.coordinates(width=0.52, height=0.55)


            for i in range(2):
                # 军团副本战斗
                self.coordinates(width=0.5, height=0.88)
                time.sleep(0.5)
                self.coordinates(width=0.7, height=0.85)

                time.sleep(1.3)
                self.coordinates(width=0.95, height=0.84)
                time.sleep(1.5)
                self.coordinates(width=0.7, height=0.88)

            # 点击返回
            self.coordinates(width=0.07, height=0.96)
            time.sleep(0.5)
            # 点击炼宝阁入口
            self.coordinates(width=0.82, height=0.18)
            time.sleep(0.5)
            self.coordinates(width=0.43, height=0.95)
            time.sleep(0.5)
            self.coordinates(width=0.5, height=0.88)






