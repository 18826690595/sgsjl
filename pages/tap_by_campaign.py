import time

from core.utils import Utils


class Tap_By_Campaign(Utils):

    def __init__(self, driver):
        super().__init__(driver)

    def campaign_page(self):
        for i in range(5):
            is_zhengzhan = self.get_snapshot(file_path="../page_png/zhengzhan.png", compare=True)
            if is_zhengzhan is True:
                return True
            self.coordinates(width=0.035, height=0.95)
            time.sleep(1)
        print("无法进入征战页面")
        return None

    def in_campaign_page(self):
        is_home = self.Page_Percent()
        if is_home is True:
            # 文字识别点击征战
            page_name = "../page_png/home.png"
            button_name = "征战"
            self.find_game_entry(page_name, button_name)
            return True
        else:
            print("无法进入征战页面")
            return None

    def revenue(self):
        # 点击征战收益
        time.sleep(0.3)
        self.coordinates(width=0.2, height=0.7)
        time.sleep(0.5)

        # 判断当前是否在征战收益页面
        is_zhengzhan_shouyi = self.get_snapshot(file_path="../page_png/zhengzhan_shouyi.png", compare=True)

        if is_zhengzhan_shouyi is True:
            self.coordinates(width=0.7, height=0.83)
            time.sleep(1)
            # 判断游历值溢出页面
            is_youli_yichu = self.get_snapshot(file_path="../page_png/youli_yichu.png", compare=True,
                                                     threshold=0.7, page_name="收益溢出")
            if is_youli_yichu is True:
                self.coordinates(width=0.7, height=0.63)
            # 判断领取收益页面
            is_guaji_jiangli = self.get_snapshot(file_path="../page_png/guaji_jiangli.png", compare=True,
                                                       page_name="领取收益")
            if is_guaji_jiangli is True:
                self.coordinates(width=0.07, height=0.96)

                time.sleep(5)
                # 判断升级页面
                is_shengji = self.get_snapshot(file_path="../page_png/shengji.png", compare=True,
                                                     page_name="升级")
                if is_shengji is True:
                    self.coordinates(width=0.07, height=0.96)

            time.sleep(1)

            # 循环快速采摘
            for i in range(5):
                # 第一次点击
                # if i == 2:
                #     time.sleep(5)
                self.coordinates(width=0.3, height=0.83)
                time.sleep(1)

                is_shouyi_tancai = self.get_snapshot(file_path="../page_png/shouyi_tancai.png", compare=True,
                                                           threshold=0.7, page_name="快速探采")
                if is_shouyi_tancai is True:
                    self.coordinates(width=0.5, height=0.73)
                    time.sleep(0.5)

                    # 判断游历值溢出页面
                    is_youli_yichu = self.get_snapshot(file_path="../page_png/youli_yichu.png", compare=True,
                                                             threshold=0.7, page_name="收益溢出")
                    if is_youli_yichu is True:
                        self.coordinates(width=0.7, height=0.63)
                        time.sleep(0.5)
                is_shengji = self.get_snapshot(file_path="../page_png/youli_yichu.png", compare=True,
                                                     page_name="升级")
                if is_shengji is True:
                    time.sleep(1)
                    self.coordinates(width=0.7, height=0.83)
        else:
            print("未找到领取收益/快速探采")

    # 派遣
    def dispatch(self, is_mark=None):
        # 点击返回征战页面
        if self.campaign_page() is not True:
            self.in_campaign_page()

        self.coordinates(width=0.92, height=0.25)
        for i in range(4):
            self.coordinates(width=0.75, height=0.86)

        pq_png = [
            # "../page_png/pq/jjl.png",  # 将军令
            "../page_png/pq/mjl.png",  # 名将令
            # "../page_png/pq/sp.png",  # 武将碎片
            "../page_png/pq/yb.png"  # 元宝
        ]

        y_png = [660, 899, 1138, 1377]
        for i in  range(20):
            time.sleep(0.3)

            # 遍历查找满足派遣条件的任务
            for y in y_png:
                for pq in pq_png:
                    # # 如果是将军令则置信度调为0.5,，其他为0.7
                    # if pq == pq_png[0]:
                    #     threshold_num = 0.5
                    # else:
                    #     threshold_num = 0.7
                    is_pq = self.compare_image_region(template_path=pq, region=(597, y, 150, 150), page_name=pq, threshold=0.7, is_click=False)
                    if is_pq is True:
                        if y == y_png[0]:
                            print(f"第1个派遣：(597, {y}, 300, 400)")
                            self.coordinates(width=0.85, height=0.38)

                        if y == y_png[1]:
                            print(f"第2个派遣：(597, {y}, 300, 400)")
                            self.coordinates(width=0.85, height=0.51)

                        if y == y_png[2]:
                            print(f"第3个派遣：(597, {y}, 300, 400)")
                            self.coordinates(width=0.85, height=0.64)

                        if y == y_png[3]:
                            print(f"第4个派遣：(597, {y}, 300, 400)")
                            self.coordinates(width=0.85, height=0.77)
                        time.sleep(1)
                        is_no_tl = self.compare_image_region(template_path="../page_png/pq/no_tl.png", region=(200, 820, 600, 80), page_name="无派遣体力", threshold=0.7, is_click=False)
                        if is_no_tl is True:
                            print("无体力派遣")
                            return True
                        time.sleep(0.5)
                        is_paichu = self.get_snapshot(file_path="../page_png/paichu.png", compare=True, page_name='手动派遣页面')
                        if is_paichu is True:
                            self.coordinates(width=0.28, height=0.81)
                            self.coordinates(width=0.72, height=0.81)
                            time.sleep(0.5)
                        break
            time.sleep(0.5)
            # 点击刷新
            self.coordinates(width=0.5, height=0.86)
            time.sleep(0.5)
            # 判断如果出现稀有度任务提示弹窗则点击确定
            self.compare_image_region(template_path="../page_png/pq/tishi.png", region=(550, 1130, 400, 130), page_name="稀有度提示弹窗")
            print(f"第{i+1}次循环结束")





    # 征战
    def Page_Campaign(self):
        # 进入征战页面
        self.in_campaign_page()
        # 执行征战收益操作
        self.revenue()
        # 执行派遣
        self.dispatch()



