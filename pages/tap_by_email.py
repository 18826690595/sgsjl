import time

from core.utils import Utils
from pages.tap_by_percent import Tap_By_Percent


class Tap_By_Email(Utils):

    def __init__(self, driver):
        super().__init__(driver)


    # 邮件
    def page_mail(self):
        # 初始化点击主城
        self.Page_Percent()
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            pass

