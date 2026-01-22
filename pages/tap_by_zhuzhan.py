import time

from core.utils import Utils


class Tap_By_ZhuZhan():

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)

    # 神兽
    def Super_Monster(self):
        """按屏幕百分比点击"""
        try:
            # 点击主城
            is_home = self.utils.Page_Percent()
            if is_home is True:
                self.utils.coordinates(width=0.4, height=0.96)
                time.sleep(0.5)
                self.utils.coordinates(width=0.4, height=0.85)
                time.sleep(0.5)
                self.utils.coordinates(width=0.4, height=0.96)
                time.sleep(0.5)
                # 点击礼包
                self.utils.coordinates(width=0.93, height=0.25)
                time.sleep(0.5)
                for i in range(2):
                    self.utils.coordinates(width=0.86, height=0.38)
                    time.sleep(0.5)
                for i in range(2):
                    self.utils.coordinates(width=0.86, height=0.52)
                    time.sleep(0.5)

            elif is_home is False:
                return False




        except Exception as e:
            print(f"执行流程时出错: {str(e)}")
            return False

    # 红颜
    def zhuzhan_beauty(self):
        """按屏幕百分比点击"""
        try:
            # 点击主城
            is_home = self.utils.Page_Percent()
            if is_home is True:
                self.utils.coordinates(width=0.4, height=0.96)
                time.sleep(0.5)
                self.utils.swipe_screen(0.5, 0.8, 0.5, 0.2)
                time.sleep(1)
                # 点击红颜入口
                self.utils.coordinates(width=0.8, height=0.48)
                time.sleep(0.5)
                is_beauty = self.utils.get_snapshot(file_path="../page_png/beauty.png", compare=True, page_name="红颜")
                if is_beauty is True:
                    self.utils.coordinates(width=0.4, height=0.96)
                    time.sleep(0.5)

                    # 循环游历没点12次挑战一次副本
                    for a in range(3):
                        for i in range(13):
                            # 点击游历
                            self.utils.coordinates(width=0.5, height=0.84)
                            time.sleep(1.5)

                        time.sleep(1)
                        self.utils.coordinates(width=0.5, height=0.73)
                        time.sleep(1)
                        self.utils.coordinates(width=0.6, height=0.88)
                        time.sleep(1.3)
                        self.utils.coordinates(width=0.95, height=0.84)
                        time.sleep(1.5)
                        self.utils.coordinates(width=0.7, height=0.88)
                        time.sleep(1)












        except Exception as e:
            print(f"执行流程时出错: {str(e)}")
            return False

    def zhuzhan_all(self):
        self.Super_Monster()
        self.zhuzhan_beauty()