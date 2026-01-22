import time

from core.utils import Utils


class Tap_By_Campaign:

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)

    def campaign_page(self):
        for i in range(5):
            is_zhengzhan = self.utils.get_snapshot(file_path="../page_png/zhengzhan.png", compare=True)
            if is_zhengzhan is True:
                return True
            self.utils.coordinates(width=0.035, height=0.95)
            time.sleep(1)
        print("无法进入征战页面")
        return None

    def in_campaign_page(self):
        is_home = self.utils.Page_Percent()
        if is_home is True:
            # 文字识别点击征战
            page_name = "../page_png/home.png"
            button_name = "征战"
            self.utils.find_game_entry(page_name, button_name)
            return True
        else:
            print("无法进入征战页面")
            return None

    def revenue(self):
        # 点击征战收益
        self.utils.coordinates(width=0.2, height=0.7)
        time.sleep(0.5)

        # 判断当前是否在征战收益页面
        is_zhengzhan_shouyi = self.utils.get_snapshot(file_path="../page_png/zhengzhan_shouyi.png", compare=True)
        if is_zhengzhan_shouyi is True:
            self.utils.coordinates(width=0.7, height=0.83)
            time.sleep(1)
            # 判断游历值溢出页面
            is_youli_yichu = self.utils.get_snapshot(file_path="../page_png/youli_yichu.png", compare=True,
                                                     threshold=0.7, page_name="收益溢出")
            if is_youli_yichu is True:
                self.utils.coordinates(width=0.7, height=0.63)
            # 判断领取收益页面
            is_guaji_jiangli = self.utils.get_snapshot(file_path="../page_png/guaji_jiangli.png", compare=True,
                                                       page_name="领取收益")
            if is_guaji_jiangli is True:
                self.utils.coordinates(width=0.07, height=0.96)

                time.sleep(5)
                # 判断升级页面
                is_shengji = self.utils.get_snapshot(file_path="../page_png/shengji.png", compare=True,
                                                     page_name="升级")
                if is_shengji is True:
                    self.utils.coordinates(width=0.07, height=0.96)

            time.sleep(1)

            # 循环快速采摘
            for i in range(5):
                # 第一次点击
                # if i == 2:
                #     time.sleep(5)
                self.utils.coordinates(width=0.3, height=0.83)
                time.sleep(1)

                is_shouyi_tancai = self.utils.get_snapshot(file_path="../page_png/shouyi_tancai.png", compare=True,
                                                           threshold=0.7, page_name="快速探采")
                if is_shouyi_tancai is True:
                    self.utils.coordinates(width=0.5, height=0.73)
                    time.sleep(0.5)

                    # 判断游历值溢出页面
                    is_youli_yichu = self.utils.get_snapshot(file_path="../page_png/youli_yichu.png", compare=True,
                                                             threshold=0.7, page_name="收益溢出")
                    if is_youli_yichu is True:
                        self.utils.coordinates(width=0.7, height=0.63)
                        time.sleep(0.5)
                is_shengji = self.utils.get_snapshot(file_path="../page_png/youli_yichu.png", compare=True,
                                                     page_name="升级")
                if is_shengji is True:
                    time.sleep(1)
                    self.utils.coordinates(width=0.7, height=0.83)
        else:
            print("未找到领取收益/快速探采")


    def dispatch(self, is_mark=None):
        # 点击返回征战页面
        if self.campaign_page():
            self.utils.coordinates(width=0.92, height=0.25)
            for i in range(4):
                self.utils.coordinates(width=0.75, height=0.86)
            for i in  range(5):
                if i >= 1:
                    # 判断如果出现稀有度任务提示弹窗则点击取消
                    is_Rare_task_hint = self.utils.get_snapshot(file_path="../page_png/Rare_task_hint.png", compare=True)
                    if is_Rare_task_hint is True:
                        self.utils.coordinates(width=0.3, height=0.62)

                for i in range(1,5):
                    if i == 1:
                        self.utils.coordinates(width=0.85, height=0.38)
                    if i == 2:
                        self.utils.coordinates(width=0.85, height=0.51)
                    if i == 3:
                        self.utils.coordinates(width=0.85, height=0.64)
                    if i == 4:
                        self.utils.coordinates(width=0.85, height=0.77)
                    time.sleep(0.5)
                    is_paichu = self.utils.get_snapshot(file_path="../page_png/paichu.png", compare=True)
                    if is_paichu is True:
                        self.utils.coordinates(width=0.28, height=0.81)
                        self.utils.coordinates(width=0.72, height=0.81)
                        time.sleep(0.5)
                if self.campaign_page():
                    self.utils.coordinates(width=0.92, height=0.25)
                time.sleep(0.5)
                # 点击刷新
                self.utils.coordinates(width=0.5, height=0.86)


    # 征战
    def Page_Campaign(self):
        # 进入征战页面
        self.in_campaign_page()
        # 执行征战收益操作
        self.revenue()
        # 执行派遣
        self.dispatch()



