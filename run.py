


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
        self.utils.get_snapshot(file_path="./page_png/Dungeon.png")



if __name__ == "__main__":
    run = Run()
    run.get_run()