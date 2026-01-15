from pages.page_barrier import Page_Barrier

from pages.tap_by_login import Tap_By_Login
from core.base_app import AppAutoManager
from pages.tap_by_outlogin import Tap_By_OutLogin


class Run():
    def __init__(self):
        self.base_app = AppAutoManager()
        self.driver = self.base_app.appium_init()
        # 实例化页面组件
        self.tap_by_login = Tap_By_Login(self.driver)
        self.tap_by_outlogin = Tap_By_OutLogin(self.driver)
        self.page_barrier = Page_Barrier(self.driver)

    def get_run(self):
        """主运行方法"""
        try:
            for i in range(202508026, 202508029):
                # self.tap_by_login.Page_Login(username=i, password="python")
                #
                # self.tap_by_outlogin.Page_Out_Login()

                break

        except Exception as e:
            print(e)
        finally:
            self.driver.quit()


if __name__ == "__main__":
    run = Run()
    run.get_run()

