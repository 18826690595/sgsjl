import time

from selenium.webdriver.common.by import By

from core.utils import Utils


class Tap_By_Login:
    username_input = By.XPATH, "//android.widget.EditText[@hint='账号（6-36位数字或字母）']"
    password_input = By.XPATH, "//android.widget.EditText[@hint='密码（6-18位数字或字母）']"
    login_button = By.XPATH, "//android.widget.Button[@text='登录']"
    agreement_checkbox = By.XPATH, "//android.widget.Image[@bounds='[159,1419][186,1443]']"

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(self.driver)


    def find_el(self, feature, max_retries=3):
        retry_count = 0
        while retry_count < max_retries:
            try:
                return self.driver.find_element(*feature)
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    raise
                time.sleep(0.5)

    def Page_Login(self, username, password="python"):
        time.sleep(3)  # 增加等待时间
        try:
            is_login = self.utils.get_snapshot(file_path="../page_png/login.png", compare=True)
            if is_login is True:
                max_retries = 3
                retry_count = 0

                while retry_count < max_retries:
                    try:
                        # 输入账号
                        self.find_el(self.username_input).clear()
                        self.find_el(self.username_input).send_keys(username)

                        # 输入密码
                        self.find_el(self.password_input).clear()
                        self.find_el(self.password_input).send_keys(password)

                        # 点击登录按钮
                        self.find_el(self.login_button).click()
                        break
                    except Exception as e:
                        retry_count += 1
                        print(f"⚠️ 登录尝试 {retry_count}/{max_retries} 失败: {str(e)}")
                        time.sleep(1)
                        if retry_count == max_retries:
                            raise
                # # 输入账号
                # self.driver.coordinates(width=0.5, height=0.4, input_text=username)
                #
                # # 输入密码
                # self.driver.coordinates(width=0.5, height=0.5, input_text=password)
                # # 点击登录
                # self.driver.coordinates(width=0.5, height=0.6)
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
                self.utils.coordinates(width=0.92, height=0.2)



        except Exception as e:
            print(f"❌ 登录流程出错: {str(e)}")
            page_xml = self.driver.page_source
            file_path = "../xml_word/test"
            if file_path:
                xml_path = file_path.replace('.png', '.xml') if file_path.endswith('.png') else file_path + '.xml'
                with open(xml_path, 'w', encoding='utf-8') as f:
                    f.write(page_xml)
                print(f"✅ 页面XML文档已保存到: {xml_path}")
            raise


