from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException  # Add this import
import time
import urllib3
from selenium.common.exceptions import WebDriverException

def app_login(username, password):
    # 设置Desired Capabilities
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "127.0.0.1:7555"
    options.app_package = "com.wxbz_sgshjz.ks10"
    options.app_activity = ".MainActivity"
    options.automation_name = "UiAutomator2"
    options.no_reset = True

    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # 修改为新的Appium端点（适用于Appium 2.0+）
        driver = webdriver.Remote(
            "http://localhost:4723",  # 移除了/wd/hub路径
            options=options
        )
        # 设置各种超时时间
        driver.implicitly_wait(10)  # 设置隐式等待为10秒
        # 移除了 set_script_timeout 调用
        # 移除了 set_page_load_timeout 调用，因为Appium Android驱动不支持
        
        # 等待元素出现并输入用户名
        username_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.EditText[@hint='账号（6-36位数字或字母）']"))
        )
        # 添加重试机制
        retries = 3
        for attempt in range(retries):
            try:
                username_element.clear()  # 先清空输入框
                username_element.send_keys(username)
                break
            except StaleElementReferenceException:
                if attempt == retries - 1:
                    raise
                # 重新获取元素
                username_element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//android.widget.EditText[@hint='账号（6-36位数字或字母）']"))
                )
        
        # 输入密码
        password_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.EditText[@hint='密码（6-18位数字或字母）']"))
        )
        # 同样添加重试机制
        for attempt in range(retries):
            try:
                password_element.clear()
                password_element.send_keys(password)
                break
            except StaleElementReferenceException:
                if attempt == retries - 1:
                    raise
                password_element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//android.widget.EditText[@hint='密码（6-18位数字或字母）']"))
                )
        
        # 点击登录按钮
        login_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//android.widget.Button[@text='登录']"))
        )
        login_button.click()
        
        # 等待登录完成，使用显式等待代替固定sleep
        WebDriverWait(driver, 20).until(
            lambda d: d.find_element(By.XPATH, "//*[contains(@text,'欢迎') or contains(@text,'首页')]")
        )
        #
        print("登录成功！")
        
    except WebDriverException as e:
        if "The requested resource could not be found" in str(e):
            print("Appium server connection failed. Please check:")
            print("1. Appium server is running (run 'appium')")
            print("2. Appium server is accessible at http://localhost:4723")
            print("3. The URL endpoint is correct (should be '/wd/hub')")
            print("4. No firewall is blocking the connection")
        else:
            print(f"WebDriver error: {str(e)}")
        print("详细错误信息:")
        import traceback
        traceback.print_exc()
        print("请检查:")
        print("1. Appium服务版本是否匹配 (appium --version)")
        print("2. 设备/模拟器是否响应 (adb shell input keyevent 82)")
        print("3. App是否已正确安装 (adb shell pm list packages)")
        print("4. 元素定位是否正确 (使用uiautomatorviewer检查)")
    finally:
        if 'driver' in locals():
            driver.quit()

# 使用示例
if __name__ == "__main__":
    app_login("202508001", "python")