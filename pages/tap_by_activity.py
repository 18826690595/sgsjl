import time

from core.utils import Utils
from pages.base_page import BasePage


class Tap_By_Activity(Utils):

    def __init__(self, driver):
        super().__init__(driver)


    # 活动日常购买操作
    def lq_lb(self, activity_name,activity_icon, lb_path, mf_path, yb_path, yb_qd_path, region_lb,region_mf,region_yb, region_yb_qd, for_num=None):
        """
        :param for_num: 是否循环第二次
        :param activity_icon: 活动icon图片路径
        :param activity_name: 活动名称
        :param yb_qd_path: 元宝购买弹窗确认按钮对比图片路径
        :param region_yb_qd: 元宝购买确定弹窗
        :param region_yb: 元宝购买比对坐标
        :param region_mf: 免费按钮比对坐标
        :param region_lb: 礼包按钮比对坐标
        :param lb_path: 礼包按钮对比图片路径
        :param mf_path: 免费按钮对比图片路径
        :param yb_path: 元宝购买按钮对比图片路径
        :return: 执行成功返回True，否则返回False
        """
        # 检查不在首页则结束执行
        if for_num is None:
            is_home = self.Page_Percent()
            if is_home is not True:
                return False


            self.match_and_click(template_path=activity_icon,
                                                  region=(0, 190, 1080, 600),
                                                  page_name=activity_name, is_click=True)

        time.sleep(0.8)
        is_lb = self.compare_image_region(template_path=lb_path, region=region_lb, page_name="礼包")
        time.sleep(0.5)
        if is_lb is True:
            self.compare_image_region(template_path=mf_path, region=region_mf, page_name="领取免费礼包")
            self.coordinates(width=0.96, height=0.5)
            time.sleep(0.5)
            self.compare_image_region(template_path=yb_path, region=region_yb, page_name="购买元宝礼包")
            time.sleep(1)
            self.compare_image_region(template_path=yb_qd_path, region=region_yb_qd, page_name="购买元宝礼包确定")
            time.sleep(0.3)
            for i in range(2):
                self.coordinates(width=0.3, height=0.95)

            return is_lb

        else:
            print(f"未匹配上{is_lb}按钮，跳过")
            return False




    # 厉兵秣马
    def horses_operation(self):
        # 点击完成任务
        for i in range(12):
            self.coordinates(width=0.9, height=0.38)
        # 领取每日奖励
        is_pay_win = self.get_snapshot(file_path="../page_png/activity/horses_page.png", compare=True)
        if is_pay_win is True:
            self.coordinates(width=0.75, height=0.88)
            time.sleep(0.5)
            self.coordinates(width=0.9, height=0.38)
        # 如果出现支付弹窗则点击关闭弹窗
        is_horses_pay_win = self.get_snapshot(file_path="../page_png/activity/horses_page.png", compare=True)
        if is_horses_pay_win is True:
            self.coordinates(width=0.835, height=0.345)



    # 皇榜
    def notice_operation(self):
        is_home = self.Page_Percent()
        if is_home is True:
            is_notice = self.match_and_click(template_path="../page_png/activity/Notice_page.png", region=(0, 0, 1080, 600),
                                       page_name="皇榜", is_click=True)
            if is_notice is True:
                # 点击每日奖励入口
                time.sleep(1)
                self.coordinates(width=0.88, height=0.28)
                time.sleep(0.5)
                # 点击领取免费奖励
                self.coordinates(width=0.82, height=0.42)
            else:
                print("not notice")

    # 帝魂帝尊操作
    def emperor_operation(self):

        huodong = {
            "activity_icon": "../page_png/activity/emperor_page.png",
            "lb_path": "../page_png/activity/dihun/lb.png",
            "mf_path": "../page_png/activity/dihun/lb_mf.png",
            "yb_path": "../page_png/activity/dihun/lb_yb.png",
            "activity_name": "帝魂",
            "region_page": (860, 1860, 180, 250),
            "region_lb": (930, 230, 120, 300),
            "region_mf": (800, 780, 200, 50),
            "region_yb": (800, 780, 200, 50)
        }

        for i in range(2):
            if i == 1:
                self.coordinates(width=0.7, height=0.96)
                time.sleep(0.5)
            self.lq_lb(activity_name=huodong["activity_name"],activity_icon=huodong["activity_icon"], lb_path=huodong["lb_path"], mf_path=huodong["mf_path"], yb_path=huodong["yb_path"],
                       yb_qd_path=None, region_lb=huodong["region_lb"],
                       region_mf=huodong["region_mf"], region_yb=huodong["region_yb"],
                       region_yb_qd=None)

        return True

    # 鸿运
    def hongyun(self):
        huodong = {
            "activity_icon": "../page_png/activity/armoury_page.png",
            "lb_path" : "../page_png/activity/armoury_page_lb.png",
            "mf_path" : "../page_png/activity/armoury_lb_mf.png",
            "yb_path" : "../page_png/activity/armoury_lb_yb.png",
            "yb_qd_path" : "../page_png/activity/armoury_lb_qd_yb.png",
            "activity_name" : "锦囊妙计",
            "region_page" : (850, 1780, 180, 180),
            "region_lb" : (940, 435, 120, 120),
            "region_mf" : (780, 750, 230, 100),
            "region_yb" : (780, 1028, 230, 100),
            "region_yb_qd" : (600, 1150, 296, 90)
        }

        self.lq_lb(activity_name=huodong["activity_name"], activity_icon=huodong["activity_icon"],
                   lb_path=huodong["lb_path"], mf_path=huodong["mf_path"], yb_path=huodong["yb_path"],
                   yb_qd_path=huodong["yb_qd_path"], region_lb=huodong["region_lb"],
                   region_mf=huodong["region_mf"], region_yb=huodong["region_yb"],
                   region_yb_qd=huodong["region_yb_qd"])

        return True


    # 神魔
    def shenmo(self):
        huodong = {
            "activity_icon": "../page_png/activity/demon_page.png",
            "lb_path": "../page_png/activity/shenmo/lb.png",
            "mf_path": "../page_png/activity/shenmo/lb_mf.png",
            "yb_path": "../page_png/activity/shenmo/lb_yb.png",
            "activity_name": "神魔",
            "region_lb": (965, 345, 68, 50),
            "region_mf": (800, 780, 200, 50),
            "region_yb": (800, 780, 200, 50),
        }

        for_num = None
        for i in range(2):
            if i == 1:
                self.coordinates(width=0.7, height=0.96)
                for_num = 1
                time.sleep(0.5)
            self.lq_lb(activity_name=huodong["activity_name"], activity_icon=huodong["activity_icon"],
                       lb_path=huodong["lb_path"], mf_path=huodong["mf_path"], yb_path=huodong["yb_path"],
                       yb_qd_path=None, region_lb=huodong["region_lb"],
                       region_mf=huodong["region_mf"], region_yb=huodong["region_yb"],
                       region_yb_qd=None,for_num=for_num)

        return True


    # 税收
    def shuishou(self):
        is_home = self.Page_Percent()
        if is_home is True:
            self.coordinates(width=0.55, height=0.05)
            time.sleep(1)
            for i in range(3):
                self.coordinates(width=0.2, height=0.71)
        else:
            print("不在首页跳过税收操作")


    #
    # 报名阵营夺魁
    def zhenying(self):
        # 每周1、3、5报名
        is_home = self.Page_Percent()
        if is_home is True:
            self.coordinates(width=0.2, height=0.5)


    # 逐鹿中原
    def zhulu(self):
        # 每周2、4、6执行
        is_home = self.Page_Percent()
        if is_home is True:
            self.match_and_click(template_path="../page_png/activity/zhulu.png", region=(0, 0, 1080, 600),
                                       page_name="逐鹿中原", is_click=True)

            time.sleep(0.5)
            self.coordinates(width=0.75, height=0.95)

            # 冠军
            time.sleep(0.3)
            self.coordinates(width=0.15, height=0.65)
            time.sleep(0.3)
            self.coordinates(width=0.8, height=0.3)

            # 亚军
            time.sleep(0.3)
            self.coordinates(width=0.4, height=0.65)
            time.sleep(0.3)
            self.coordinates(width=0.8, height=0.4)

            # 季军
            time.sleep(0.3)
            self.coordinates(width=0.65, height=0.65)
            time.sleep(0.3)
            self.coordinates(width=0.8, height=0.5)

            # 殿军
            time.sleep(0.3)
            self.coordinates(width=0.9, height=0.65)
            time.sleep(0.3)
            self.coordinates(width=0.8, height=0.6)


    # 净世真灵
    def jinshizhenling(self):
        huodong = {
            "activity_icon": "../page_png/activity/zhenling/zhenling.png",
            "lb_path": "../page_png/activity/dihun/lb.png",
            "mf_path": "../page_png/activity/dihun/lb_mf.png",
            "yb_path": "../page_png/activity/dihun/lb_yb.png",
            "activity_name": "净世真灵",
            "region_page": (860, 1860, 180, 250),
            "region_lb": (930, 230, 120, 300),
            "region_mf": (800, 780, 200, 50),
            "region_yb": (800, 780, 200, 50)
        }

        self.lq_lb(activity_name=huodong["activity_name"], activity_icon=huodong["activity_icon"], lb_path=huodong["lb_path"], mf_path=huodong["mf_path"], yb_path=huodong["yb_path"],
                   yb_qd_path=None, region_lb=huodong["region_lb"],
                   region_mf=huodong["region_mf"], region_yb=huodong["region_yb"],
                   region_yb_qd=None)

        return True




    # 八阵奇图
    def bazhen(self):
        huodong = {
            "activity_icon": "../page_png/activity/bazhenqitu.png",
            "lb_path": "../page_png/activity/dihun/lb.png",
            "mf_path": "../page_png/activity/dihun/lb_mf.png",
            "yb_path": "../page_png/activity/dihun/lb_mf.png",  # 暂时不做元宝付费
            "activity_name": "八阵奇图",
            "region_page": (860, 1860, 180, 250),
            "region_lb": (930, 230, 120, 300),
            "region_mf": (800, 780, 200, 50),
            "region_yb": (800, 780, 200, 50)
        }

        self.lq_lb(activity_name=huodong["activity_name"], activity_icon=huodong["activity_icon"], lb_path=huodong["lb_path"], mf_path=huodong["mf_path"], yb_path=huodong["yb_path"],
                   yb_qd_path=None, region_lb=huodong["region_lb"],
                   region_mf=huodong["region_mf"], region_yb=huodong["region_yb"],
                   region_yb_qd=None)

        return True

    # 帝谕天命
    def tianming(self):
        huodong = {
            "activity_icon": "../page_png/activity/tianming.png",
            "lb_path": "../page_png/activity/dihun/lb.png",
            "mf_path": "../page_png/activity/dihun/lb_mf.png",
            "yb_path": "../page_png/activity/dihun/lb_yb.png",
            "activity_name": "帝谕天命",
            "region_page": (860, 1860, 180, 250),
            "region_lb": (930, 230, 120, 300),
            "region_mf": (800, 780, 200, 50),
            "region_yb": (800, 780, 200, 50)
        }

        self.lq_lb(activity_name=huodong["activity_name"], activity_icon=huodong["activity_icon"],
                   lb_path=huodong["lb_path"], mf_path=huodong["mf_path"], yb_path=huodong["yb_path"],
                   yb_qd_path=None, region_lb=huodong["region_lb"],
                   region_mf=huodong["region_mf"], region_yb=huodong["region_yb"],
                   region_yb_qd=None)

        return True






    # 九州争霸
    # 领取巅峰夺魁奖励
    # 巅峰夺魁竞猜





    def all_activity(self):
        # 神魔
        self.shenmo()
        # 鸿运
        self.hongyun()
        # 皇榜
        self.notice_operation()
        # 帝魂
        self.emperor_operation()
        # # 净世真灵
        # self.jinshizhenling()
        # # 八阵奇图
        # self.bazhen()



