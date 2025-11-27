import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Campaign:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()




    # 征战
    def Page_Campaign(self):
        # 初始化点击主城
        self.utils.Page_Percent(5)

        is_home = self.utils.get_snapshot(file_path="../page_png/home.png", compare=True, threshold=0.5)
        if is_home is True:
            # 文字识别点击征战
            page_name = "../page_png/home.png"
            button_name = "征战"
            self.utils.find_game_entry(page_name, button_name)

            # 点击征战收益
            time.sleep(0.5)
            self.utils.coordinates(width=0.2, height=0.7)
            time.sleep(1)

            # 判断当前是否在征战收益页面
            zhengzhan_shouyi = self.utils.get_snapshot(file_path="../page_png/zhengzhan_shouyi.png", compare=True)
            if zhengzhan_shouyi is True:
                self.utils.coordinates(width=0.7, height=0.83)
                time.sleep(1)
                # 判断游历值溢出页面
                youli_yichu = self.utils.get_snapshot(file_path="../page_png/youli_yichu.png", compare=True, threshold=0.7, page_name="收益溢出")
                if youli_yichu is True:
                    self.utils.coordinates(width=0.7, height=0.63)
                # 判断领取收益页面
                guaji_jiangli = self.utils.get_snapshot(file_path="../page_png/guaji_jiangli.png", compare=True, page_name="领取收益")
                if guaji_jiangli is True:
                    self.utils.coordinates(width=0.07, height=0.96)

                    time.sleep(5)
                    # 判断升级页面
                    shengji = self.utils.get_snapshot(file_path="../page_png/shengji.png", compare=True, page_name="升级")
                    if shengji is True:
                        self.utils.coordinates(width=0.07, height=0.96)

                time.sleep(1)

                # 循环快速采摘
                for i in range(5):
                    # 第一次点击
                    if i == 2:
                        time.sleep(5)
                    self.utils.coordinates(width=0.3, height=0.83)
                    time.sleep(1)

                    shouyi_tancai = self.utils.get_snapshot(file_path="../page_png/shouyi_tancai.png", compare=True, threshold=0.7, page_name="快速探采")
                    if shouyi_tancai is True:
                        self.utils.coordinates(width=0.5, height=0.73)
                        time.sleep(0.5)

                        # 判断游历值溢出页面
                        youli_yichu = self.utils.get_snapshot(file_path="../page_png/youli_yichu.png", compare=True, threshold=0.7, page_name="收益溢出")
                        if youli_yichu is True:
                            self.utils.coordinates(width=0.7, height=0.63)



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