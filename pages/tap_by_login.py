import time

from selenium.webdriver.common.by import By

from sgmjl.core.utils import Utils
from sgmjl.pages.tap_by_percent import Tap_By_Percent


class Tap_By_Login:

    def __init__(self, driver=None):
        self.driver = driver
        self.utils = Utils()

    def Page_Login(self, username, password="python"):
        try:
            is_login = self.utils.get_snapshot(file_path="../page_png/login.png", compare=True)
            if is_login is True:
                max_retries = 3
                retry_count = 0

                while retry_count < max_retries:
                    try:
                        # 输入账号
                        account_field = self.utils.find_element(
                            by=By.XPATH,
                            value="//android.widget.EditText[@hint='账号（6-36位数字或字母）']"
                        )
                        if account_field:
                            account_field.clear()
                            account_field.send_keys(username)

                        # 输入密码
                        password_field = self.utils.find_element(
                            by=By.XPATH,
                            value="//android.widget.EditText[@hint='密码（6-18位数字或字母）']"
                        )
                        if password_field:
                            password_field.clear()
                            password_field.send_keys(password)

                        # 点击登录按钮
                        login_button = self.utils.find_element(
                            by=By.XPATH,
                            value="//android.widget.Button[@text='登录']"
                        )
                        if login_button:
                            login_button.click()
                            break

                    except Exception as e:
                        retry_count += 1
                        print(f"⚠️ 登录尝试 {retry_count}/{max_retries} 失败: {str(e)}")
                        time.sleep(1)
                        if retry_count == max_retries:
                            raise
                # # 输入账号
                # self.utils.coordinates(width=0.5, height=0.4, input_text=username)
                #
                # # 输入密码
                # self.utils.coordinates(width=0.5, height=0.5, input_text=password)
                # # 点击登录
                # self.utils.coordinates(width=0.5, height=0.6)
                time.sleep(0.5)
                # 同意服务条款
                self.utils.coordinates(width=0.5, height=0.7)
                time.sleep(0.5)
                # 跳过手机号绑定
                self.utils.coordinates(width=0.16, height=0.24)

                # 确认进入游戏页面
                for i in range(10):
                    time.sleep(0.5)
                    games_door = self.utils.get_snapshot(file_path="../page_png/games_door.png", compare=True)
                    if games_door is True:
                        break
                    self.utils.coordinates(width=0.07, height=0.96)
                time.sleep(0.5)
                # 点击进入游戏
                self.utils.coordinates(width=0.5, height=0.8)
                time.sleep(8)

                # 关闭弹窗(需要增加判断是否出现弹窗)
                self.utils.coordinates(width=0.85, height=0.28)
                time.sleep(0.5)
                self.utils.coordinates(width=0.92, height=0.2)


        except Exception as e:
            print(f"❌ 登录流程出错: {str(e)}")
            raise



# 修改测试部分
if __name__ == "__main__":
    test = Tap_By_Login()
    test.Page_Login("202508003")
    # ut = Utils()
    # ut.lgs()
