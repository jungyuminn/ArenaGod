import os
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

BASE_PATH = get_base_path()
RESOURCES_PATH = os.path.join(BASE_PATH, 'resources')
IMAGES_PATH = os.path.join(RESOURCES_PATH, 'images')
FONTS_PATH = os.path.join(RESOURCES_PATH, 'fonts')
DATA_PATH = os.path.join(BASE_PATH, 'data')

CHAMPIONS_PATH = os.path.join(IMAGES_PATH, 'champions')
CACHE_PATH = os.path.join(RESOURCES_PATH, 'cache')

PRETENDARD_REGULAR = os.path.join(FONTS_PATH, 'Pretendard-Regular.ttf')
PRETENDARD_BOLD = os.path.join(FONTS_PATH, 'Pretendard-Bold.ttf')
PRETENDARD_MEDIUM = os.path.join(FONTS_PATH, 'Pretendard-Medium.ttf')

def ensure_directories():
    for path in [RESOURCES_PATH, IMAGES_PATH, FONTS_PATH, DATA_PATH, CHAMPIONS_PATH, CACHE_PATH]:
        os.makedirs(path, exist_ok=True)

ensure_directories()