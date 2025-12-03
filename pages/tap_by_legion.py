import time

from core.utils import Utils


class Tap_By_Legion:

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)


    # 军团
    def Page_Legion(self, duration=300):
        # 初始化点击主城
        is_home = self.utils.Page_Percent(5)
        if is_home is True:
            # 点击军团入口
            self.utils.coordinates(width=0.58, height=0.96)
            time.sleep(1)

            is_lianmeng = self.utils.get_snapshot(file_path="../page_png/lianmeng.png", compare=True)
            if is_lianmeng is True:
                # 点击军团、联盟入口
                self.utils.coordinates(width=0.5, height=0.2)
                time.sleep(1)

            # 点击祭祀入口
            self.utils.coordinates(width=0.36, height=0.72)
            time.sleep(1)
            # 点击祭祀
            self.utils.coordinates(width=0.5, height=0.78)
            time.sleep(1)
            # 点击祭祀确定
            self.utils.coordinates(width=0.7, height=0.6)
            time.sleep(1)

            for i in range(2):
                # 点击关闭祭祀页面
                print("点击关闭祭祀页面")
                self.utils.coordinates(width=0.91, height=0.19)

            # 点击军团副本入口
            self.utils.coordinates(width=0.52, height=0.55)

            # x = window_size['width'] * 0.52
            # y = window_size['height'] * 0.55
            # self.driver.tap([(x, y)], duration)
            # print(f"📍 已通过坐标 ({x:.0f}, {y:.0f}) 点击军团副本入口")

            for i in range(2):
                # 军团副本战斗
                self.utils.coordinates(width=0.5, height=0.88)

                self.utils.coordinates(width=0.7, height=0.85)

                time.sleep(1.3)
                self.utils.coordinates(width=0.95, height=0.84)
                time.sleep(1.5)
                self.utils.coordinates(width=0.7, height=0.88)

            # 点击返回
            self.utils.coordinates(width=0.07, height=0.96)

            # 点击盟主挑战切磋
            time.sleep(1)
            self.utils.coordinates(width=0.15, height=0.7)

            self.utils.coordinates(width=0.60, height=0.86)

            time.sleep(1)
            self.utils.coordinates(width=0.7, height=0.85)

            time.sleep(1.3)
            self.utils.coordinates(width=0.95, height=0.84)

            time.sleep(1.5)
            self.utils.coordinates(width=0.25, height=0.88)

