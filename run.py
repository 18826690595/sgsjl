


import pyautogui
import time

from core.base_app import AppAutoManager
from core.utils import Utils


class Run():
    def __init__(self):
        self.base_app = AppAutoManager()
        self.driver = self.base_app.appium_init()
        self.utils = Utils(self.driver)

    def get_run(self):
        try:
            # self.utils.get_snapshot(file_path="./page_png/Dungeon.png")
            for i in range(10):
                self.utils.coordinates(width=0.2, height=0.96)
        except Exception as e:
            print(e)
        finally:
            self.base_app


if __name__ == "__main__":
    run = Run()
    run.get_run()
