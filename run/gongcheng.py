import time

from pages.page_gongcheng import Page_GC
from pages.tap_by_login import Tap_By_Login
from core.base_app import AppAutoManager
from pages.tap_by_outlogin import Tap_By_OutLogin


class Run:
    def __init__(self):
        self.base_app = AppAutoManager()
        self.driver = self.base_app.appium_init()
        # # 实例化页面组件
        self.tap_by_login = Tap_By_Login(self.driver)
        self.tap_by_outlogin = Tap_By_OutLogin(self.driver)
        self.page_activity = Page_GC(self.driver)

    def get_run(self):
        """主运行方法"""
        global start_time

        try:

            # 记录开始时间
            start_time = time.time()
            # is_week = datetime.today().weekday()
            # print(is_week)
            # for i in range(202508001, 202508029):
            #     self.tap_by_login.Page_Login(username=i, password="python")
            #
            self.page_activity.gongcheng()
            #
            #     self.tap_by_outlogin.Page_Out_Login()
            #

                    # break
            # else:
            #     print(f"今天是周{is_week}不执行中原")

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

