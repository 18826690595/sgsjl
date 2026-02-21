


import pyautogui
import time

from core.base_app import AppAutoManager
from core.utils import Utils

from core.base_app import AppAutoManager

# 派遣
# region=(597, 899, 150, 150)





class Run():
    def __init__(self):
        self.base_app = AppAutoManager()
        self.driver = self.base_app.appium_init()
        self.utils = Utils(self.driver)

    def get_run(self):
        try:
            # "../page_png/armoury_page.png",  # 天降鸿运
            # "../page_png/horses_page.png",  # 厉兵牧马
            # "../page_png/Notice_page.png",  # 皇榜
            # "../page_png/emperor_page.png",  # 帝魂
            # "../page_png/demon_page.png"  # 神魔  660 899 1138 1377
            self.utils.get_snapshot(file_path="./page_png/activity/dihun/test.png", region=(930, 230, 120, 300), overwrite=True)
            # self.utils.find_game_entry(button_name='挑战')

            # is_home = self.utils.get_snapshot(file_path="./page_png/demon_page.png", compare=True, page_name="主城")
            # print(is_home)

            #
            # for i in range(1):
            #     self.utils.coordinates(width=0.75, height=0.88)

            # self.utils.click_icon("./page_png/PK_icon.png")



        except Exception as e:
            print(e)
        finally:
            self.base_app.quit(self.driver)


if __name__ == "__main__":
    run = Run()
    run.get_run()
