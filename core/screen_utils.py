class ScreenUtils:
    """屏幕操作相关工具"""
    def __init__(self, driver):
        self.driver = driver
        self.window_size = self._get_window_size()
    
    def swipe(self, start_width, start_height, end_width, end_height):
        """滑动屏幕"""
        # ... 实现原swipe_screen方法 ...
    
    def tap_coordinates(self, width_percent, height_percent):
        """按百分比点击坐标"""
        # ... 实现原coordinates方法的核心功能 ...
    
    def take_screenshot(self, file_path=None, region=None):
        """截图"""
        # ... 实现原get_snapshot的截图部分 ...