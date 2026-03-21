
from core.utils import Utils
from core.base_app import AppAutoManager

class Page_Percentage(AppAutoManager):
    def __init__(self):
        super().__init__()
        # # 实例化页面组件
        self.driver = self.appium_init()
        self.utils = Utils(self.driver)

    def page_percentage(self):
        """主运行方法"""
        try:
            self.utils.Page_Percent()

        except Exception as e:
            print(e)
        finally:
            self.driver.quit()


if __name__ == "__main__":
    run = Page_Percentage()
    run.page_percentage()

