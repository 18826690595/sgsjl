import time
# from sgmjl.core.utils import Utils
from pages.tap_by_login import Tap_By_Login
from pages.tap_by_percent import Tap_By_Percent


class Run():
    def __init__(self):
        super().__init__()
        # 实例化必要组件
        self.tap_by_login = Tap_By_Login(self.driver)
        self.tap_by_percent = Tap_By_Percent(self.driver)

    def get_run(self):
        """主运行方法"""
        for i in range(202508001, 202508029):
            self.tap_by_login.Page_Login(username=i, password="python")
            break
            # 点击主城
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