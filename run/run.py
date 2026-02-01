import time

from pages.tap_by_activity import Tap_By_Activity
from pages.tap_by_arena import Tap_By_Arena
from pages.tap_by_chat import Tap_By_Chat
from pages.tap_by_email import Tap_By_Email
from pages.tap_by_good_friend import Tap_By_Good_Friend
from pages.tap_by_legion import Tap_By_Legion
from pages.tap_by_login import Tap_By_Login
from pages.tap_by_campaign import Tap_By_Campaign
from core.base_app import AppAutoManager
from pages.tap_by_outdoors import Tap_By_OutDoors
from pages.tap_by_outlogin import Tap_By_OutLogin
from pages.tap_by_recruit import Tap_By_Recruit
from pages.tap_by_store import Tap_By_Store
from pages.tap_by_task import Tap_By_Task
from pages.tap_by_trials_tower import Tap_By_Trials_Tower
from pages.tap_by_vip import Tap_By_VIP
from pages.tap_by_zhuzhan import Tap_By_ZhuZhan


class Run():
    def __init__(self):
        self.base_app = AppAutoManager()
        self.driver = self.base_app.appium_init()
        # self.utils = Utils(self.driver)

        # 实例化页面组件
        self.tap_by_login = Tap_By_Login(self.driver)
        self.tap_by_vip = Tap_By_VIP(self.driver)
        self.tap_by_trials_tower = Tap_By_Trials_Tower(self.driver)
        self.tap_by_task = Tap_By_Task(self.driver)
        self.tap_by_store = Tap_By_Store(self.driver)
        self.tap_by_recruit = Tap_By_Recruit(self.driver)
        self.tap_by_outlogin = Tap_By_OutLogin(self.driver)
        self.tap_by_outdoors = Tap_By_OutDoors(self.driver)
        self.tap_by_legion = Tap_By_Legion(self.driver)
        self.tap_by_good_friend = Tap_By_Good_Friend(self.driver)
        self.tap_by_email = Tap_By_Email(self.driver)
        self.tap_by_chat = Tap_By_Chat(self.driver)
        self.tap_by_campaign = Tap_By_Campaign(self.driver)
        self.tap_by_arena = Tap_By_Arena(self.driver)
        self.Tap_By_ZhuZhan = Tap_By_ZhuZhan(self.driver)
        # self.tap_by_activity = Tap_By_Activity(s·elf.driver)

    def get_run(self):
        """主运行方法"""
        start_time = time.time()  # 记录开始时间
        try:
            for i in range(202508003, 202508029):
                # 登录
                log_login = self.tap_by_login.Page_Login(username=i, password="python")
                if log_login is False:
                    print(i)
                    break
                # 领取vip奖励
                self.tap_by_vip.Page_Vip()
                # 好友日常
                self.tap_by_good_friend.Page_good_friend()
                # 发送世界聊天
                self.tap_by_chat.Page_Chat()
                # 竞技场
                self.tap_by_arena.Page_Arena()
                # 斗塔
                self.tap_by_trials_tower.Page_Trials_Tower()
                # 名将招募
                self.tap_by_recruit.Page_Recruit()
                # 商店购买
                self.tap_by_store.Page_Store()
                # 军团任务
                self.tap_by_legion.Page_Legion()
                # 野外
                self.tap_by_outdoors.Page_OutDoors()
                # 征战
                self.tap_by_campaign.Page_Campaign()
                # 领取任务奖励
                self.tap_by_task.Page_Task()
                # 助战
                self.Tap_By_ZhuZhan.zhuzhan_all()

                # 未开发
                # self.tap_by_activity.Page_Activity()

                #
                self.tap_by_outlogin.Page_Out_Login()


        except Exception as e:
            print(e)
        finally:
            self.driver.quit()
            end_time = time.time()  # 记录结束时间
            elapsed_time = end_time - start_time  # 计算总耗时(秒)

            # 转换为时分秒格式
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)
            print(f"方法执行耗时: {hours}小时 {minutes}分钟 {seconds}秒")


if __name__ == "__main__":
    run = Run()
    run.get_run()

