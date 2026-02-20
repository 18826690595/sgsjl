class ImageUtils:
    """图像处理相关工具"""
    def __init__(self, driver):
        self.driver = driver
    
    def find_text_on_screen(self, target_text, threshold=0.7):
        """识别屏幕上的文字"""
        # ... 实现类似find_game_entry和click_text_on_screen的功能 ...
    
    def click_icon(self, icon_path, threshold=0.5):
        """识别并点击图标"""
        # ... 实现原click_icon方法 ...
    
    def compare_images(self, template_path, region=None, threshold=0.7):
        """比较图像区域"""
        # ... 实现原compare_image_region方法 ...