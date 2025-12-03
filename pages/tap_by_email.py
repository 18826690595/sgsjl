import time

from core.utils import Utils
from pages.tap_by_percent import Tap_By_Percent


class Tap_By_Email:

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)


    # 邮件
    def page_mail(self, duration=300):
        # 初始化点击主城
        self.utils.Page_Percent(5)
        page_name = "./page_png/home.png"
        is_home = self.utils.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            pass


# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Email()
    test.page_mail()