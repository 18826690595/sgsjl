import time

from core.utils import Utils

from core.base_app import AppAutoManager



class Run():
    def __init__(self):
        self.base_app = AppAutoManager()
        self.driver = self.base_app.appium_init()
        self.utils = Utils(self.driver)

    def get_run(self):
        try:
            # self.utils.get_snapshot(file_path="./page_png/demon_page.png")
            # self.utils.find_game_entry(button_name='挑战')

            # is_home = self.utils.get_snapshot(file_path="./page_png/demon_page.png", compare=True, page_name="主城")
            # print(is_home)


            for i in range(1):
                self.utils.coordinates(width=0.75, height=0.88)

            # self.utils.click_icon("./page_png/PK_icon.png")



        except Exception as e:
            print(e)
        finally:
            self.base_app.quit(self.driver)


if __name__ == "__main__":
    run = Run()
    run.get_run()
