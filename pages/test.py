import time

from core.utils import Utils


class Tap_By_test:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils(self.driver)

    # 返回点击主城
    def test(self):
        # self.utils.coordinates(width=0.338, height=0.37

        # x_list = [18,172,326,480,633,783]
        # y_list = [210,410,610]
        # for y in y_list:
        #     for x in x_list:
        #         # 过滤点击空白区域
        #         if y == y_list[0] and x is x_list[4]:
        #             print(f"跳过（{x, y}）")
        #             break
        #         else:
        #             is_beauty = self.utils.compare_image_region(template_path="../page_png/Notice_page.png", region=(x, y, 123, 150), page_name="截图区域")
        #             if is_beauty is True:
        #                 print(f"({x}, {y}, 123, 150)=======1")
        #                 self.utils.Page_Percent()
        #             else:
        #                 print(f"({x}, {y}, 123, 150)=======0")

        # is_beauty = self.utils.compare_image_region(template_path="../page_png/pq/yb.png", region=(597, 899, 150, 150), page_name="锦囊礼包", is_click=False)
        is_beauty = self.utils.match_and_click(template_path="../page_png/activity/demon_page.png", region=(0, 0, 1080, 600), page_name="锦囊礼包", is_click=True)
        if is_beauty is True:
            print("1")
        else:
            print("0")


    def some_method(self):
        # 可以直接调用 OpenCV 方法
        result = self.utils.match_and_click("../page_png/activity/demon_page.png", (0,0,100,100))
        print(result)

