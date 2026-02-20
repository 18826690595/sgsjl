from core.base_opencv import OpenCVTemplateMatcher
from core.utils import Utils


class BasePage:

    def __init__(self, driver):
        self.matcher = Utils(driver)
        
    def some_method(self):
        # 可以直接调用 OpenCV 方法
        result = self.matcher.match_and_click("../page_png/activity/demon_page.png", (0,0,100,100))
        print(result)


