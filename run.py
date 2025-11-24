import time
from core.utils import Utils
from pages.tap_by_login import Tap_By_Login
from pages.tap_by_percent import Tap_By_Percent


class Run(Utils):
    def __init__(self):
        super().__init__()
        # 实例化
        self.tap_by_login = Tap_By_Login(self.driver)
        self.tap_by_percent = Tap_By_Percent(self.driver)

        # self.tap_by_vip = Tap_By_VIP(self.driver)
        # self.tap_by_good_friend = Tap_By_Good_Friend(self.driver)
        # self.tap_by_Chat = Tap_By_Chat(self.driver)
        # self.tap_by_percent = Tap_By_Percent(self.driver)
        # self.tap_by_trials_tower = Tap_By_Trials_Tower(self.driver)
        # self.tap_by_arena = Tap_By_Arena(self.driver)
        # self.tap_by_percent = Tap_By_Recruit(self.driver)
        # self.tap_by_percent = Tap_By_Percent(self.driver)
        # self.tap_by_percent = Tap_By_Percent(self.driver)
        # self.tap_by_percent = Tap_By_Percent(self.driver)
        # self.tap_by_percent = Tap_By_Percent(self.driver)
        # self.tap_by_percent = Tap_By_Percent(self.driver)
        # self.tap_by_percent = Tap_By_Percent(self.driver)
        # self.tap_by_percent = Tap_By_Percent(self.driver)

    def get_run(self):
        """主运行方法"""
        for i in range(202508001,202508029):
            self.tap_by_login.Page_Login(username=i, password="python")
            break
            # 点击主城
            # self.tap_by_percent.Page_Percent()


            # self.tap_by_percent.Page_Percent()
            # self.tap_by_percent.Page_Percent()
            # self.tap_by_percent.Page_Percent()
            # self.tap_by_percent.Page_Percent()
            # self.tap_by_percent.Page_Percent()

if __name__ == "__main__":
    try:
        app_manager = Run()
        app_manager.get_run()

    except Exception as e:
        print(e)
    finally:
        if 'app_manager' in locals():
            app_manager.quit()