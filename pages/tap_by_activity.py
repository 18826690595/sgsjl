import time

from numpy.f2py.crackfortran import endifs

from core.utils import Utils
from pages.tap_by_percent import Tap_By_Percent


class Tap_By_Activity:

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)


    # 活动日常购买操作
    def lq_lb(self, lb_path, mf_path, yb_path, yb_qd_path, region_lb,region_mf,region_yb, region_yb_qd):
        """
        :param yb_qd_path: 元宝购买弹窗确认按钮对比图片路径
        :param region_yb_qd: 元宝购买确定弹窗
        :param region_yb: 元宝购买比对坐标
        :param region_mf: 免费按钮比对坐标
        :param region_lb: 礼包按钮比对坐标
        # :param region_page: 页面比对坐标
        # :param page_path: 进入页面的对比图片路径
        :param lb_path: 礼包按钮对比图片路径
        :param mf_path: 免费按钮对比图片路径
        :param yb_path: 元宝购买按钮对比图片路径
        # :param page_name: 页面名称
        :return: 执行成功返回True，否则返回False
        """
        time.sleep(0.5)
        is_lb = self.utils.compare_image_region(template_path=lb_path, region=region_lb, page_name="礼包")
        time.sleep(0.5)
        if is_lb is True:
            self.utils.compare_image_region(template_path=mf_path, region=region_mf, page_name="领取免费礼包")
            self.utils.coordinates(width=0.96, height=0.5)
            time.sleep(0.5)
            self.utils.compare_image_region(template_path=yb_path, region=region_yb, page_name="购买元宝礼包")
            time.sleep(1)
            self.utils.compare_image_region(template_path=yb_qd_path, region=region_yb_qd, page_name="购买元宝礼包确定")
            time.sleep(0.3)
            for i in range(2):
                self.utils.coordinates(width=0.55, height=0.95)

            return is_lb

        else:
            print(f"未匹配上{is_lb}按钮，跳过")
            return False




    # 厉兵秣马
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
        huodong = {
            "page_path": "../page_png/armoury_page_inner.png",
            "lb_path": "../page_png/armoury_page_lb.png",
            "mf_path": "../page_png/armoury_lb_mf.png",
            "yb_path": "../page_png/armoury_lb_yb.png",
            "page_name": "锦囊妙计",
            "region_page": (850, 1780, 180, 180),
            "region_lb": (940, 435, 120, 120),
            "region_mf": (780, 750, 230, 100),
            "region_yb": (780, 1028, 230, 100)
        }
        res = self.lq_lb(lb_path=huodong["lb_path"], mf_path=huodong["mf_path"],
                         yb_path=huodong["yb_path"], region_lb=huodong["region_lb"],
                         region_mf=huodong["region_mf"], region_yb=huodong["region_yb"])
        return res

    # 鸿运
    def hongyun(self):

        huodong = {
            "page_path": "../page_png/armoury_page_inner.png",
            "lb_path" : "../page_png/armoury_page_lb.png",
            "mf_path" : "../page_png/armoury_lb_mf.png",
            "yb_path" : "../page_png/armoury_lb_yb.png",
            "yb_qd_path" : "../page_png/armoury_lb_qd_yb.png",
            "page_name" : "锦囊妙计",
            "region_page" : (850, 1780, 180, 180),
            "region_lb" : (940, 435, 120, 120),
            "region_mf" : (780, 750, 230, 100),
            "region_yb" : (780, 1028, 230, 100),
            "region_yb_qd" : (600, 1150, 296, 90)
        }

        res = self.lq_lb(lb_path=huodong["lb_path"], mf_path=huodong["mf_path"], yb_path=huodong["yb_path"],yb_qd_path=huodong["yb_qd_path"], region_lb=huodong["region_lb"],region_mf=huodong["region_mf"],region_yb=huodong["region_yb"],region_yb_qd=huodong["region_yb_qd"])
        return res

    # 神魔
    def shenmo(self):
        huodong = {
            "page_path": "../page_png/armoury_page_inner.png",
            "lb_path": "../page_png/armoury_page_lb.png",
            "mf_path": "../page_png/armoury_lb_mf.png",
            "yb_path": "../page_png/armoury_lb_yb.png",
            "page_name": "锦囊妙计",
            "region_page": (850, 1780, 180, 180),
            "region_lb": (940, 435, 120, 120),
            "region_mf": (780, 750, 230, 100),
            "region_yb": (780, 1028, 230, 100)
        }

        is_page_inner = self.utils.compare_image_region(template_path=huodong["page_path"], region=huodong["region_page"],
                                                                page_name=huodong["page_name"])
        if is_page_inner is True:
            for i in range(2):
                self.lq_lb(lb_path=huodong["lb_path"], mf_path=huodong["mf_path"],
                                 yb_path=huodong["yb_path"], region_lb=huodong["region_lb"], region_mf=huodong["region_mf"], region_yb=huodong["region_yb"])
                time.sleep(0.1)
                self.utils.coordinates(width=0.55, height=0.05)

            return is_page_inner


    # 税收
    def shuishou(self):
        is_home = self.utils.Page_Percent()
        if is_home is True:
            self.utils.coordinates(width=0.55, height=0.05)
            time.sleep(1)
            for i in range(3):
                self.utils.coordinates(width=0.2, height=0.71)
        else:
            print("不在首页跳过税收操作")

    # 活动
    def Page_Activity(self):
        is_home = self.utils.Page_Percent()
        if is_home is True:
            # 税收
            self.shuishou()
            self.utils.Page_Percent()
            # 遍历点击活动区域
            activity_page = [
                "../page_png/armoury_page.png", # 天降鸿运
                "../page_png/horses_page.png",  # 厉兵牧马
                "../page_png/Notice_page.png",  # 皇榜
                "../page_png/emperor_page.png", # 帝魂
                "../page_png/demon_page.png"   # 神魔
            ]
            x_list = [18, 172, 326, 480, 633, 783]
            y_list = [210, 410, 610]
            activity_total = 0
            for y in y_list:
                for x in x_list:
                    # 过滤点击空白区域
                    if y == y_list[0] and x is x_list[4]:
                        print(f"跳过（{x, y}）")
                        break

                    print("="*150)
                    for activity_path in activity_page:
                        is_activity_page = self.utils.compare_image_region(template_path=activity_path, region=(x, y, 300, 400), page_name=activity_path, threshold=0.5)
                        # 判断是否匹配到活动页面
                        if is_activity_page is True:
                            # 根据不同活动执行不同操作
                            # 鸿运
                            print(f"activity_path:{activity_path}\nactivity_page:{activity_page}")

                            # 天降鸿运
                            if activity_path == activity_page[0]:
                                is_hongyun = self.hongyun()
                                if is_hongyun is True:
                                    print("天降鸿运匹配成功")
                                    activity_total = activity_total + 1
                            # 神魔
                            elif activity_path == activity_page[1]:
                                self.shenmo()
                                print("神魔匹配成功")
                                activity_total = activity_total + 1
                            # 厉兵牧马
                            elif activity_path == activity_page[2]:
                                self.horses_operation()
                                print("厉兵牧马匹配成功")

                                activity_total = activity_total + 1
                            # 皇榜
                            elif activity_path == activity_page[3]:
                                # self.Notice_operation()
                                print("皇榜匹配成功")

                                activity_total = activity_total + 1
                            # 帝魂帝尊
                            elif activity_path == activity_page[4]:
                                # self.emperor_operation()
                                print("帝魂帝尊匹配成功")

                                activity_total = activity_total + 1
                            if activity_total == 5:
                                return
                            else:
                                print(activity_total,"="*100)
                    self.utils.Page_Percent()
                    time.sleep(0.5)





