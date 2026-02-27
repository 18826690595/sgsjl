
import time
from datetime import datetime
from time import sleep

from core.utils import Utils



class Tap_By_OutDoors:

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)

    # 判断是否在野外页面
    def tap_by_outdoors(self):
        # 如果在野外页面则返回True
        for i in range(5):
            is_outdoors1 = self.utils.get_snapshot(file_path="../page_png/outdoors1.png", compare=True)
            if is_outdoors1 is True:
                print(f"在野外页面则返回True{i}")
                return True
            else:
                self.utils.coordinates(width=0.07, height=0.96)
                time.sleep(0.5)

        # 保底校验在野外页面
        self.utils.Page_Percent()
        print("============")
        self.utils.coordinates(width=0.76, height=0.94)
        time.sleep(0.5)
        is_outdoors1 = self.utils.get_snapshot(file_path="../page_png/outdoors1.png", compare=True)
        if is_outdoors1 is True:
            return True


    # 荆州
    def JingZhou(self, ):
        outdoors = self.tap_by_outdoors()
        if outdoors is True:

            # 点击荆州
            self.utils.coordinates(width=0.7, height=0.2)
            time.sleep(0.5)
            # 点击挑战
            self.utils.coordinates(width=0.8, height=0.5)
            self.utils.coordinates(width=0.8, height=0.64)
            self.utils.coordinates(width=0.8, height=0.76)
            # 点击一键派遣
            # self.utils.coordinates(width=0.7, height=0.5)
            # 点击出战
            time.sleep(1)
            self.utils.coordinates(width=0.33, height=0.85)
            self.utils.coordinates(width=0.66, height=0.85)
            time.sleep(2.5)
            # 点击跳过战斗5次
            for i in range(17):
                # 选择加成
                is_jzzy = self.utils.get_snapshot(file_path="../page_png/jz_zy.png", compare=True, threshold=0.7)
                if is_jzzy is True:
                    self.utils.coordinates(width=0.5, height=0.63)
                    time.sleep(1.5)

                self.utils.coordinates(width=0.95, height=0.84)
                time.sleep(1)


            time.sleep(1)
            # 点击返回玩法
            self.utils.coordinates(width=0.7, height=0.88)

            time.sleep(0.5)
            self.utils.coordinates(width=0.8, height=0.64)
            time.sleep(0.5)
            for i in range(2):
                self.utils.coordinates(width=0.88, height=0.38)
                time.sleep(0.5)

            for i in range(2):
                self.utils.coordinates(width=0.62, height=0.37)
                time.sleep(0.5)

            for i in range(2):
                self.utils.coordinates(width=0.338, height=0.37)
                time.sleep(0.5)

        else:
            print("不在野外页面")
            return



    # 激战虎牢
    def rage_at_tiger_lair(self):
        outdoors = self.tap_by_outdoors()
        if outdoors is True:
            # 点击激战虎牢
            self.utils.coordinates(width=0.38, height=0.7)
            # 点击领取排位奖励(需要判断是否有弹窗，调用图像识别太慢了，直接点击两次)
            for i in range(3):
                self.utils.coordinates(width=0.7, height=0.3)
                time.sleep(0.5)

            # 挑战两次
            for i in range(2):
                for y in range(2):
                    self.utils.coordinates(width=0.5, height=0.95)
                time.sleep(0.5)
                self.utils.coordinates(width=0.6, height=0.88)
                time.sleep(1.3)
                self.utils.coordinates(width=0.95, height=0.84)
                time.sleep(1.5)
                self.utils.coordinates(width=0.7, height=0.88)
                # 第二次执行不需要等待
                if i == 0:
                    time.sleep(1)

    # 火烧赤壁
    def ScarredCliff(self):
        is_today = datetime.today().weekday()
        if is_today % 2 == 1:
            outdoors = self.tap_by_outdoors()
            if outdoors is True:
                self.utils.coordinates(width=0.3, height=0.5)
                # 需要添加检验是否可以执行扫荡
                time.sleep(0.3)
                self.utils.coordinates(width=0.9, height=0.7)

                time.sleep(0.3)
                self.utils.coordinates(width=0.5, height=0.65)
            return True
        else:
            print("非执行日不执行火烧赤壁")
            return False

    # 副本-高效率
    def fuben(self):
        # 判断当前是否在野外页面
        is_outdoors1 = self.tap_by_outdoors()
        if is_outdoors1 is True:
            # 点击副本入口
            self.utils.coordinates(width=0.3, height=0.2)
            time.sleep(0.5)

            # 循环4个类型的副本
            for i in range(4):
                # is_Dungeon = self.utils.get_snapshot(file_path="../page_png/Dungeon.png",
                #                                               compare=True, threshold=0.5)
                # if is_Dungeon is True:
                # 0锦囊、1装备、2经验、3银币， saodang_mun = 6为扫荡次数
                if i == 0:
                    self.utils.coordinates(width=0.43, height=0.94)
                    saodang_mun = 5
                elif i == 1:
                    self.utils.coordinates(width=0.58, height=0.94)
                    saodang_mun = 3
                elif i == 2:
                    self.utils.coordinates(width=0.73, height=0.94)
                    saodang_mun = 4
                elif i == 3:
                    self.utils.coordinates(width=0.88, height=0.94)
                    saodang_mun = 5


                # 循环扫荡3次
                for j in range(saodang_mun):
                    time.sleep(0.5)
                    self.utils.coordinates(width=0.85, height=0.45)
                    self.utils.coordinates(width=0.85, height=0.85)
                    time.sleep(0.3)
                    #     # 只扫荡免费次数
                    self.utils.coordinates(width=0.2, height=0.96)


    # 副本（效率太慢）已废弃
    def	Dungeon(self):

        # 判断当前是否在野外页面
        is_outdoors1 = self.tap_by_outdoors()
        if is_outdoors1 is True:
            # 点击副本入口
            self.utils.coordinates(width=0.3, height=0.2)
            time.sleep(0.5)

            # 循环4个类型的副本
            for i in range(4):
                # is_Dungeon = self.utils.get_snapshot(file_path="../page_png/Dungeon.png",
                #                                               compare=True, threshold=0.5)
                # if is_Dungeon is True:
                    # 0锦囊、1装备、2经验、3银币
                    if i == 0:
                        self.utils.coordinates(width=0.43, height=0.94)
                    elif i == 1:
                        self.utils.coordinates(width=0.58, height=0.94)
                    elif i == 2:
                        self.utils.coordinates(width=0.73, height=0.94)
                    elif i == 3:
                        self.utils.coordinates(width=0.88, height=0.94)

                    # 循环扫荡3次
                    for j in range(6):
                        time.sleep(0.5)
                        # self.utils.coordinates(width=0.85, height=0.45)
                        # time.sleep(0.5)

                        is_lb = self.utils.compare_image_region(template_path="../page_png/outdoor/fuben/saodang.png", region=(790, 810, 230, 90),
                                                                page_name=f"扫荡{i}", is_click=False,threshold=0.9)

                        if is_lb is True:
                            self.utils.coordinates(width=0.85, height=0.45)
                            time.sleep(0.5)
                        #     # # 点击元宝扫荡
                        #     # self.utils.coordinates(width=0.7, height=0.60)
                        #
                        #     # 只扫荡免费次数
                            self.utils.coordinates(width=0.2, height=0.96)
                        #     break
                        else:
                            break
                        #     # time.sleep(0.5)
                        #     self.utils.coordinates(width=0.2, height=0.96)

    # 攻城略地税收
    # 云梦泽
    def Yunmengze(self):
        is_outdoors1 = self.tap_by_outdoors()
        if is_outdoors1 is True:
            self.utils.coordinates(width=0.75, height=0.8)
            time.sleep(0.5)

            for i in range(2):
                # 点击野怪猎人
                self.utils.coordinates(width=0.8, height=0.18)
                time.sleep(1)
                # 图像识别点击野怪猎人
                self.utils.click_icon(icon_path="../page_png/yeguai1.png")
                time.sleep(0.5)
                # 点击挑战
                self.utils.coordinates(width=0.5, height=0.73)
                time.sleep(0.5)
                # 点击出战
                self.utils.coordinates(width=0.7, height=0.85)
                time.sleep(1.5)
                # 点击跳过战斗
                self.utils.coordinates(width=0.95, height=0.84)
                time.sleep(1.5)
                # 点击返回玩法
                self.utils.coordinates(width=0.75, height=0.88)




            for i in range(2):
                # 点击野怪驻军
                self.utils.coordinates(width=0.8, height=0.21)
                time.sleep(1)
                # 图像识别点击野怪驻军
                self.utils.click_icon(icon_path="../page_png/yeguai1.png")
                time.sleep(0.5)
                # 点击挑战
                self.utils.coordinates(width=0.5, height=0.73)
                time.sleep(0.5)
                # 点击出战
                self.utils.coordinates(width=0.7, height=0.85)
                time.sleep(1.5)
                # 点击跳过战斗
                self.utils.coordinates(width=0.95, height=0.84)
                time.sleep(1.5)
                # 点击返回玩法
                self.utils.coordinates(width=0.75, height=0.88)
                time.sleep(1)

    # 七星遗迹
    def qixingyiji(self):
        self.tap_by_outdoors()
        self.utils.swipe_screen(0.5, 0.8, 0.5, 0.2)
        time.sleep(1.5)
        self.utils.coordinates(width=0.3, height=0.2)
        time.sleep(0.5)
        is_yiji = self.utils.get_snapshot(file_path="../page_png/yiji.png", compare=True)
        if is_yiji is True:
            for i in range(15):
                # 重新点击进入遗迹界面
                if i >= 1:
                    self.utils.coordinates(width=0.3, height=0.2)
                    time.sleep(0.5)

                # 判断如果已经结束则退出
                if i >= 6:
                    is_yiji_done = self.utils.compare_image_region(template_path="../page_png/outdoor/yiji/chonzhi.png", region=(430, 1400, 230, 250),
                                                                page_name=f"扫荡{i}", is_click=False,threshold=0.9)
                    if is_yiji_done is True:
                        print("遗迹任务已完成！！！")
                        break


                # 点击摇骰子
                self.utils.coordinates(width=0.5, height=0.8)
                time.sleep(0.3)

                # 第三次摇骰子选择默认元宝付费弹窗
                if i == 2:
                    self.utils.coordinates(width=0.38, height=0.52)
                    self.utils.coordinates(width=0.65, height=0.62)
                    time.sleep(0.3)


                # 否则返回上级页面
                self.utils.coordinates(width=0.035, height=0.95)
                time.sleep(0.3)
        else:
            print("未进入七星遗迹页面，跳过流程")
            return False






    # 万象古镜
    # 九州
    # 单骑救主
    def zhaoyun(self):
        self.tap_by_outdoors()
        self.utils.swipe_screen(0.5, 0.8, 0.5, 0.2)
        time.sleep(1.5)
        self.utils.coordinates(width=0.8, height=0.5)
        time.sleep(0.5)
        is_zhaoyun = self.utils.get_snapshot(file_path="../page_png/zhaoyun.png", compare=True)
        if is_zhaoyun is True:
            self.utils.coordinates(width=0.42, height=0.95)
            time.sleep(0.5)
            self.utils.coordinates(width=0.92, height=0.17)
            time.sleep(0.5)
            for i in range(4):
                self.utils.coordinates(width=0.86, height=0.42)

        else:
            print("未找到单骑救主页面")
            return False



    # 博古通今
    def bogutongjin(self):
        res = self.tap_by_outdoors()
        print(res)
        self.utils.swipe_screen(0.5, 0.8, 0.5, 0.2)
        time.sleep(1.5)
        self.utils.coordinates(width=0.4, height=0.8)
        time.sleep(0.5)
        is_bogutongjin = self.utils.get_snapshot(file_path="../page_png/bogutongjin.png", compare=True)
        if is_bogutongjin is True:
            self.utils.coordinates(width=0.5, height=0.85)
            time.sleep(0.5)
            for i in range(3):
                self.utils.coordinates(width=0.75, height=0.95)

            time.sleep(0.5)
            self.utils.coordinates(width=0.93, height=0.2)
            time.sleep(0.5)
            # 领取收益
            for i in range(3):
                self.utils.coordinates(width=0.85, height=0.42)
                time.sleep(0.3)

            # 寻经问道领取礼包
            self.utils.coordinates(width=0.72, height=0.95)
            time.sleep(0.5)
            # for i in range(3):
            #     self.utils.coordinates(width=0.86, height=0.42)
            #     if i == 2:
            #         return True

        else:
            print("未进入博古通今页面，跳过流程")
            return False




    # 野外
    def Page_OutDoors(self):
        # 赤壁
        self.ScarredCliff()
        # 副本
        self.fuben()
        # 虎牢
        self.rage_at_tiger_lair()
        # 七星遗迹
        self.qixingyiji()
        # 单骑救主
        self.zhaoyun()
        # 博古通今
        self.bogutongjin()

        # 荆州
        # self.JingZhou()
        # self.Yunmengze()





