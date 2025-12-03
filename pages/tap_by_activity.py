import time

from core.utils import Utils
from pages.tap_by_percent import Tap_By_Percent


class Tap_By_Activity:

    def __init__(self, driver):
        self.driver = driver

    # 活动
    def Page_Activity(self):
        page_name = "./page_png/home.png"
        is_home = self.get_snapshot(file_path=page_name, compare=True)
        if is_home is True:
            # 文字识别点击

            button_name = "野外"
            self.find_game_entry(button_name=button_name)


# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Activity()
    test.Page_Activity()