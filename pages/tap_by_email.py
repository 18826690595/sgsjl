import time
from time import sleep

from core.utils import Utils
from pages.tap_by_percent import Tap_By_Percent


class Tap_By_Email(Utils):

    def __init__(self, driver):
        super().__init__(driver)

    # 邮件
    def page_mail(self):
        # 初始化点击主城
        is_home = self.Page_Percent()
        if is_home is True:
            self.compare_image_region(template_path="../page_png/Email.png", region=(0,1320,1080,220), page_name="邮件")
            time.sleep(0.5)
            is_lq = self.compare_image_region(template_path="../page_png/Email_lq.png", region=(638,1580,280,88), page_name="一键领取")
            if is_lq is True:
                for i in range(60):
                    is_windone = self.compare_image_region(template_path="../page_png/Email_windone.png", region=(338, 470, 390, 130),
                                              page_name="领取成功")
                    if is_windone is True:
                        print("邮件领取成功")
                        break

            else:
                print("未检测领取按钮")






