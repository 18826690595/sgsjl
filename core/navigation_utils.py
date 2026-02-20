class NavigationUtils:
    """页面导航相关工具"""
    def __init__(self, driver):
        self.driver = driver
        self.screen = ScreenUtils(driver)
        self.image = ImageUtils(driver)
    
    def go_to_home(self, max_attempts=10):
        """返回主城"""
        # ... 实现原Page_Percent方法 ...