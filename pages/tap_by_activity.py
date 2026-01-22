import time

from numpy.f2py.crackfortran import endifs

from core.utils import Utils
from pages.tap_by_percent import Tap_By_Percent


class Tap_By_Activity:

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)

    def activity_pay(self, bt_pay=1, activity_tpye=None):
        # 点击免费
        self.utils.coordinates(width=0.938, height=0.253)
        time.sleep(0.5)
        self.utils.coordinates(width=0.85, height=0.42)
        time.sleep(0.5)
        self.utils.coordinates(width=0.58, height=0.85)
        time.sleep(1)

        is_pay_win = self.utils.get_snapshot(file_path="../page_png/pay_win.png", compare=True)
        if is_pay_win is True:
            self.utils.coordinates(width=0.835, height=0.345)

        # 点击元宝购买
        if bt_pay == 1:
            # 如果不为空则点击第一个购买，处理神魔购买元宝永远在第一个位置
            if activity_tpye is None:
                self.utils.coordinates(width=0.85, height=0.58)
            else:
                self.utils.coordinates(width=0.85, height=0.42)
            time.sleep(0.5)
            self.utils.coordinates(width=0.58, height=0.85)

        # 如果出现支付弹窗则点击关闭弹窗
        is_pay_win = self.utils.get_snapshot(file_path="../page_png/pay_win.png", compare=True)
        if is_pay_win is True:
            self.utils.coordinates(width=0.835, height=0.345)



    # 厉兵牧马
    def horses_operation(self):
        # 点击完成任务
        for i in range(12):
            self.utils.coordinates(width=0.9, height=0.38)
        # 领取每日奖励
        is_pay_win = self.utils.get_snapshot(file_path="../page_png/horses_page.png", compare=True)
        if is_pay_win is True:
            self.utils.coordinates(width=0.75, height=0.88)
            time.sleep(0.5)
            self.utils.coordinates(width=0.9, height=0.38)
        # 如果出现支付弹窗则点击关闭弹窗
        is_horses_pay_win = self.utils.get_snapshot(file_path="../page_png/horses_page.png", compare=True)
        if is_horses_pay_win is True:
            self.utils.coordinates(width=0.835, height=0.345)



    # 皇榜
    def Notice_operation(self):
        # 点击每日奖励入口
        time.sleep(1)
        self.utils.coordinates(width=0.88, height=0.28)
        time.sleep(0.5)
        # 点击领取免费奖励
        self.utils.coordinates(width=0.82, height=0.42)

    # 帝魂帝尊操作
    def emperor_operation(self, bt_pay=1, activity_tpye=None):
        for i in range(2):
            if i == 1:
                self.utils.coordinates(width=0.3, height=0.96)
                time.sleep(1)
                is_emperor_dihun = self.utils.get_snapshot(file_path="../page_png/emperor_dihun.png", compare=True)
                if is_emperor_dihun is not True:
                    self.utils.coordinates(width=0.5, height=0.96)
                    time.sleep(0.5)
                    # 再次判断是否在帝魂页面
                    is_emperor_dihun = self.utils.get_snapshot(file_path="../page_png/emperor_dihun.png", compare=True)
                    if is_emperor_dihun is not True:
                        break


            # 帝魂购买
            self.utils.coordinates(width=0.938, height=0.2)
            time.sleep(0.5)
            self.utils.coordinates(width=0.85, height=0.42)
            time.sleep(0.5)
            self.utils.coordinates(width=0.58, height=0.85)
            time.sleep(1)

            is_pay_win = self.utils.get_snapshot(file_path="../page_png/pay_win.png", compare=True)
            if is_pay_win is True:
                self.utils.coordinates(width=0.835, height=0.345)

            # 点击元宝购买
            if bt_pay == 1:
                # 如果不为空则点击第一个购买，处理神魔购买元宝永远在第一个位置
                if activity_tpye is None:
                    self.utils.coordinates(width=0.85, height=0.58)
                else:
                    self.utils.coordinates(width=0.85, height=0.42)
                time.sleep(0.5)
                self.utils.coordinates(width=0.58, height=0.85)

            # 如果出现支付弹窗则点击关闭弹窗
            is_pay_win = self.utils.get_snapshot(file_path="../page_png/pay_win.png", compare=True)
            if is_pay_win is True:
                self.utils.coordinates(width=0.835, height=0.345)

        # 帝尊战令
        self.utils.coordinates(width=0.5, height=0.96)
        is_emperor_zhanling = self.utils.get_snapshot(file_path="../page_png/emperor_zhanling.png.png", compare=True)
        if is_emperor_zhanling is not True:
            self.utils.coordinates(width=0.68, height=0.96)
            time.sleep(0.5)
        is_emperor_zhanling = self.utils.get_snapshot(file_path="../page_png/emperor_zhanling.png.png", compare=True)
        if is_emperor_zhanling is True:
            self.utils.coordinates(width=0.65, height=0.87)
            time.sleep(0.5)
            is_emperor_task = self.utils.get_snapshot(file_path="../page_png/emperor_task.png.png",
                                                          compare=True)
            if is_emperor_task is True:
                for i in range(12):
                    self.utils.coordinates(width=0.85, height=0.443)


        else:
            print("未找到帝魂战令页面，跳过...")
            return

    def t_lgs(self):
        self.utils.Page_Percent()


    # 活动
    def Page_Activity(self):
        is_home = self.utils.Page_Percent()
        if is_home is True:
            # 税收
            self.utils.coordinates(width=0.55, height=0.05)
            time.sleep(1)
            self.utils.coordinates(width=0.2, height=0.71)
            self.utils.coordinates(width=0.5, height=0.71)
            self.utils.coordinates(width=0.8, height=0.71)
            self.utils.Page_Percent()
            # 遍历点击活动区域
            activity_page = [
                "../page_png/armoury_page.png", # 天降鸿运
                "../page_png/horses_page.png",  # 厉兵牧马
                "../page_png/Notice_page.png",  # 皇榜
                "../page_png/emperor_page.png", # 帝魂
                "../page_png/demon_page.png"   # 神魔
            ]
            x_list = [0.075, 0.22, 0.365, 0.51, 0.65, 0.795, 0.935]
            y_list = [0.145, 0.252, 0.357, 0.457]
            for y in y_list:
                for x in x_list:
                    # 过滤点击空白区域
                    if y == y_list[3] and x != x_list[5] and x != x_list[6]:
                        print(x_list[:4])
                        print(f"跳过（{x, y}）")
                        continue
                    self.utils.coordinates(width=x, height=y)
                    time.sleep(1.5)
                    activity_total = 0
                    for activity_path in activity_page:
                        is_activity_page = self.utils.get_snapshot(file_path=activity_path, compare=True, page_name=activity_path, threshold=0.3)
                        # 判断是否匹配到活动页面
                        if is_activity_page is True:
                            # 根据不同活动执行不同操作
                            # 鸿运
                            print(f"activity_path:{activity_path}\nactivity_page:{activity_page}")

                            if activity_path == activity_page[0]:
                                self.activity_pay()
                                activity_total = activity_total + 1
                            # 神魔
                            elif activity_path == activity_page[1]:
                                self.activity_pay(activity_tpye=1)
                                activity_total = activity_total + 1
                            # 厉兵牧马
                            elif activity_path == activity_page[2]:
                                self.horses_operation()
                                activity_total = activity_total + 1
                            # 皇榜
                            elif activity_path == activity_page[3]:
                                self.Notice_operation()
                                activity_total = activity_total + 1
                            # 帝魂帝尊
                            elif activity_path == activity_page[4]:
                                self.emperor_operation()
                                activity_total = activity_total + 1
                    self.utils.Page_Percent()
                    time.sleep(0.5)

                    if activity_total == 5:
                        return





