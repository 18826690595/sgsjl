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
        self.tap_by_activity = Tap_By_Activity(self.driver)

    def get_run(self):
        """主运行方法"""
        try:
            for i in range(202508002, 202508029):
                # self.tap_by_login.Page_Login(username=i, password="python")
                # self.tap_by_vip.Page_Vip()
                # self.tap_by_good_friend.Page_good_friend()
                # self.tap_by_chat.Page_Chat()
                # self.tap_by_arena.Page_Arena()
                # self.tap_by_trials_tower.Page_Trials_Tower()
                # self.tap_by_recruit.Page_Recruit()
                # self.tap_by_store.Page_Store()
                # self.tap_by_legion.Page_Legion()
                self.tap_by_outdoors.Page_OutDoors()
                # self.tap_by_campaign.Page_Campaign()
                # self.tap_by_task.Page_Task()
                #
                # self.tap_by_outlogin.Page_Out_Login()

                break
                # 点击主城
                # self.tap_by_percent.Page_Percent()

        except Exception as e:
            print(e)
        finally:
            self.driver.quit()


if __name__ == "__main__":
    run = Run()
    run.get_run()

