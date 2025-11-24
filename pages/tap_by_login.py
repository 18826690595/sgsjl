import time

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Login:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()
        self.tap_by_percent = Tap_By_Percent()

    def Page_Login(self, username, password="python"):
        try:
            page_name = "../page_png/login.png"
            is_login = self.utils.get_snapshot(file_path=page_name, compare=True)
            if is_login is True:
                # 输入账号
                self.utils.coordinates(width=0.5, height=0.4, input_text=username)
                # 输入密码
                self.utils.coordinates(width=0.5, height=0.5, input_text=password)
                # 点击登录
                self.utils.coordinates(width=0.5, height=0.6)
                time.sleep(0.5)
                # 同意服务条款
                self.utils.coordinates(width=0.5, height=0.7)
                time.sleep(0.5)
                # 跳过手机号绑定
                self.utils.coordinates(width=0.16, height=0.24)

                self.tap_by_percent.Page_Percent(2)
                time.sleep(0.5)
                # 点击进入游戏
                self.utils.coordinates(width=0.5, height=0.8)
                time.sleep(5)

                # 关闭弹窗
                self.utils.coordinates(width=0.5, height=0.8)
                time.sleep(0.5)
                self.utils.coordinates(width=0.92, height=0.2)




                # # 纯坐标点击（废弃）
                # page_name = "./page_png/games_door.png"
                # games_door = self.get_snapshot(file_path=page_name, compare=True)
                # if games_door is True:
                #     x = window_size['width'] * 0.5
                #     y = window_size['height'] * 0.8
                #     self.driver.tap([(x, y)], 300)
                #     print(f"📍 已通过坐标点击 ({x}, {y})进入游戏")
                #     time.sleep(10)


                # # 点击同意服务条款
                # print("\n🔄 点击同意服务条款...")
                # x = window_size['width'] * 0.5  # 不是0.15就是0.16
                # y = window_size['height'] * 0.7  # 不是0.24就是0.25
                # self.driver.tap([(x, y)], 300)
                # print(f"📍 已通过坐标 ({x}, {y})点击同意服务条款")
                # self.tap_by_percent(2)
                # time.sleep(1)
                #
                # # 点击跳过绑定手机号
                # print("\n🔄 点击跳过绑定手机号...")
                # x = window_size['width'] * 0.16  # 不是0.15就是0.16
                # y = window_size['height'] * 0.24  # 不是0.24就是0.25
                # self.driver.tap([(x, y)], 300)
                # print(f"📍 已通过坐标 ({x}, {y})点击跳过绑定手机号")
                # time.sleep(1)
                #
                # # 坐标点击进入游戏
                # print("\n🔄 尝试通过坐标点击进入游戏按钮...")
                # # 文字识别点击
                # page_name = "./page_png/test.jpg"
                # button_name = "进入游戏"
                # self.find_game_entry(page_name, button_name)
                #
                # # 纯坐标点击（废弃）
                # page_name = "./page_png/games_door.png"
                # games_door = self.get_snapshot(file_path=page_name, compare=True)
                # if games_door is True:
                #     x = window_size['width'] * 0.5
                #     y = window_size['height'] * 0.8
                #     self.driver.tap([(x, y)], 300)
                #     print(f"📍 已通过坐标点击 ({x}, {y})进入游戏")
                #     time.sleep(10)
                #
                # # 坐标点击关闭霸王弹窗1
                # x = window_size['width'] * 0.85
                # y = window_size['height'] * 0.28
                # self.driver.tap([(x, y)], 300)
                # print(f"📍 已通过坐标点击 ({x}, {y})关闭霸王弹窗1")
                # time.sleep(1)
                #
                # # 坐标点击关闭霸王弹窗2
                # x = window_size['width'] * 0.92
                # y = window_size['height'] * 0.2
                # self.driver.tap([(x, y)], 300)
                # print(f"📍 已通过坐标点击 ({x}, {y})关闭霸王弹窗2")
                # time.sleep(1)
                # #
                # self.tap_by_percent(3)
                # time.sleep(1)
            else:
                print("登录流程异常")

        except Exception as e:
            print(f"❌ 登录流程出错: {str(e)}")
            raise



# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Login()
    test.Page_Login("202508001")