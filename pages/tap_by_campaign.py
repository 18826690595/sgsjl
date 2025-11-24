import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Campaign:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()
        self.tap_by_percent = Tap_By_Percent()




    # 征战
    def Page_Campaign(self, duration=300):
        window_size = self.driver.get_window_size()
        # 初始化点击主城
        self.tap_by_percent(5)

        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True, threshold=0.5)
        if is_home is True:
            # 文字识别点击征战
            page_name = "./page_png/home.png"
            button_name = "征战"
            self.find_game_entry(page_name, button_name)

            # 点击征战收益
            time.sleep(0.5)
            x = window_size['width'] * 0.2
            y = window_size['height'] * 0.7
            self.driver.tap([(x, y)], 10)
            print(f"📍 已通过坐标 ({x}, {y})点击征战收益")

            time.sleep(1)
            page_name = "./page_png/zhengzhan_shouyi.png"
            zhengzhan_shouyi = self.get_snapshot(file_path=page_name, compare=True)
            if zhengzhan_shouyi is True:
                time.sleep(0.5)
                x = window_size['width'] * 0.7
                y = window_size['height'] * 0.83
                self.driver.tap([(x, y)], 10)
                print(f"📍 已通过坐标 ({x}, {y})点击领取收益")
                time.sleep(2)
                # 判断领取收益页面
                page_name = "./page_png/guaji_jiangli.png"
                guaji_jiangli = self.get_snapshot(file_path=page_name, compare=True, page_name="领取收益")
                if guaji_jiangli is True:
                    self.tap_by_percent(1)

                    time.sleep(5)
                    # 判断升级页面
                    page_name = "./page_png/shengji.png"
                    shengji = self.get_snapshot(file_path=page_name, compare=True, page_name="升级")
                    if shengji is True:
                        self.tap_by_percent(1)

                time.sleep(1)
                for i in range(5):
                    if i == 2:
                        time.sleep(5)
                    x = window_size['width'] * 0.3
                    y = window_size['height'] * 0.83
                    self.driver.tap([(x, y)], 10)
                    print(f"📍 已通过坐标 ({x}, {y})点击快速探采")
                    time.sleep(1)

                    page_name = "./page_png/shouyi_tancai.png"
                    shouyi_tancai = self.get_snapshot(file_path=page_name, compare=True, threshold=0.7,
                                                      page_name="快速探采")
                    if shouyi_tancai is True:
                        time.sleep(1)
                        x = window_size['width'] * 0.5
                        y = window_size['height'] * 0.73
                        self.driver.tap([(x, y)], 10)
                        print(f"📍 已通过坐标 ({x}, {y})点击快速收益")



            else:
                print("未找到领取收益/快速探采")



        elif is_home is False:
            print("副本页面不匹配")
        else:
            print("未知错误")


# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Campaign()
    test.Page_Campaign()