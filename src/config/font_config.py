from PyQt6.QtGui import QFont, QFontDatabase
import os
from .settings import FONTS_PATH

class FontWeight:
    THIN = 100
    EXTRA_LIGHT = 200
    LIGHT = 300
    REGULAR = 400
    MEDIUM = 500
    SEMI_BOLD = 600
    BOLD = 700
    EXTRA_BOLD = 800
    BLACK = 900

def init_fonts():
    font_files = {
        "Thin": "Pretendard-Thin.ttf",
        "ExtraLight": "Pretendard-ExtraLight.ttf",
        "Light": "Pretendard-Light.ttf",
        "Regular": "Pretendard-Regular.ttf",
        "Medium": "Pretendard-Medium.ttf",
        "SemiBold": "Pretendard-SemiBold.ttf",
        "Bold": "Pretendard-Bold.ttf",
        "ExtraBold": "Pretendard-ExtraBold.ttf",
        "Black": "Pretendard-Black.ttf"
    }

    loaded_fonts = []
    for weight, file_name in font_files.items():
        font_path = os.path.join(FONTS_PATH, file_name)
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id >= 0:
                loaded_fonts.append(weight)
    
    if not loaded_fonts:
        return None
    
    return "Pretendard"

def get_font(size=11, weight=FontWeight.REGULAR):
    font = QFont("Pretendard", size)
    font.setWeight(weight)
    return font

# 자주 사용하는 폰트 스타일 미리 정의
class FontStyle:
    TITLE = lambda size=16: get_font(size, FontWeight.BOLD)
    SUBTITLE = lambda size=14: get_font(size, FontWeight.SEMI_BOLD)
    BODY = lambda size=12: get_font(size, FontWeight.REGULAR)
    CAPTION = lambda size=11: get_font(size, FontWeight.MEDIUM)
    SMALL = lambda size=10: get_font(size, FontWeight.REGULAR)