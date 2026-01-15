import time


class Tap_By_Percent:

    def __init__(self, driver):
        self.driver = driver

    # 返回点击主城
    def Page_Percent(self, num=5, x_percent=0.07, y_percent=0.96, duration=300, desc="返回主城"):
        """按屏幕百分比点击"""
        try:
            for i in range(num):
                is_home = self.utils.get_snapshot(file_path="../page_png/home.png", compare=True)
                if is_home is True:
                    # 如果在首页则返回True
                    return True
                elif is_home is False:
                    self.utils.coordinates(width=x_percent, height=y_percent)
                    time.sleep(0.5)
                else:
                    print("未知错误")
            return False
        except Exception as e:
            print(e)
            return False

